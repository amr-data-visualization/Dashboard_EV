import sys
import can
from enum import Enum
from PySide6.QtCore import QObject, Property, Signal, QTimer, QTime, QDate
from PySide6.QtWidgets import QApplication
from PySide6.QtQml import QQmlApplicationEngine


# ---------------- Enums ----------------
class DriveMode(Enum):
    Neutral = 0
    Forward = 1
    Reverse = 2
    ForwardMap = 3
    Manual = 4


class Status(Enum):
    Disengaged = 0
    Engaged = 1


# ---------------- Dashboard Backend ----------------
class Dashboard(QObject):
    def __init__(self):
        super().__init__()

        # default values
        self._speed = 0.0
        self._drive_mode = DriveMode.Neutral
        self._dbw = Status.Disengaged
        self._brake = Status.Disengaged
        self._autopark = Status.Disengaged
        self._emergency = Status.Disengaged
        self._battery = 100
        self._date = QDate.currentDate().toString("yyyy-MM-dd")
        self._time = QTime.currentTime().toString("hh:mm:ss AP")

        # CAN bus setup
        self.bus = can.interface.Bus(channel="vcan0", interface="socketcan")
        self.notifier = can.Notifier(self.bus, [self])  # calls __call__

        # timer for clock
        self.clock_timer = QTimer()
        self.clock_timer.timeout.connect(self.update_clock)
        self.clock_timer.start(1000)

    # ---------------- Signals ----------------
    speedChanged = Signal()
    driveModeChanged = Signal()
    dbwChanged = Signal()
    brakeChanged = Signal()
    autoparkChanged = Signal()
    emergencyChanged = Signal()
    batteryChanged = Signal()
    dateChanged = Signal()
    timeChanged = Signal()

    # ---------------- Properties ----------------
    def get_speed(self): return self._speed
    def set_speed(self, value):
        if self._speed != value:
            self._speed = value
            self.speedChanged.emit()
    speed = Property(float, get_speed, set_speed, notify=speedChanged)

    def get_drive_mode(self): return self._drive_mode.name
    def set_drive_mode(self, value):
        if self._drive_mode != value:
            self._drive_mode = value
            self.driveModeChanged.emit()
    driveMode = Property(str, get_drive_mode, set_drive_mode, notify=driveModeChanged)

    def get_dbw(self): return self._dbw.name
    def set_dbw(self, value):
        if self._dbw != value:
            self._dbw = value
            self.dbwChanged.emit()
    dbw = Property(str, get_dbw, set_dbw, notify=dbwChanged)

    def get_brake(self): return self._brake.name
    def set_brake(self, value):
        if self._brake != value:
            self._brake = value
            self.brakeChanged.emit()
    brake = Property(str, get_brake, set_brake, notify=brakeChanged)

    def get_autopark(self): return self._autopark.name
    def set_autopark(self, value):
        if self._autopark != value:
            self._autopark = value
            self.autoparkChanged.emit()
    autopark = Property(str, get_autopark, set_autopark, notify=autoparkChanged)

    def get_emergency(self): return self._emergency.name
    def set_emergency(self, value):
        if self._emergency != value:
            self._emergency = value
            self.emergencyChanged.emit()
    emergency = Property(str, get_emergency, set_emergency, notify=emergencyChanged)

    def get_battery(self): return self._battery
    def set_battery(self, value):
        if self._battery != value:
            self._battery = value
            self.batteryChanged.emit()
    battery = Property(int, get_battery, set_battery, notify=batteryChanged)

    def get_date(self): return self._date
    def set_date(self, value):
        if self._date != value:
            self._date = value
            self.dateChanged.emit()
    date = Property(str, get_date, set_date, notify=dateChanged)

    def get_time(self): return self._time
    def set_time(self, value):
        if self._time != value:
            self._time = value
            self.timeChanged.emit()
    time = Property(str, get_time, set_time, notify=timeChanged)

    # ---------------- Helpers ----------------
    def update_clock(self):
        self.set_time(QTime.currentTime().toString("hh:mm:ss AP"))
        self.set_date(QDate.currentDate().toString("yyyy-MM-dd"))

    # ---------------- CAN message handler ----------------
    def __call__(self, msg):
        if msg.arbitration_id != 0x12910109:
            return

        data = msg.data

        # Decode from the signal layout
        self.set_drive_mode(DriveMode(data[0]))           # DriveModeStatus (byte 0)
        self.set_dbw(Status(data[1]))                     # DBW_SwitchStatus (byte 1)
        self.set_brake(Status(data[2]))                   # ParkingBrakeStatus (byte 2)
        self.set_autopark(Status(data[3] & 0x01))         # AutoParkBrakeStatus (bit 0 of byte 3)
        self.set_emergency(Status(data[4]))               # EmergencyStatus (byte 4)

        # Speed is at byte 6 (LSB) and byte 7 (MSB)
        raw_speed = data[6] | (data[7] << 8)
        self.set_speed(raw_speed * 0.01)                  # scale: 0.01 km/h per bit

        # Dummy battery update
        self.set_battery(max(0, self._battery - 1))


# ---------------- Main ----------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    engine = QQmlApplicationEngine()
    dashboard = Dashboard()

    engine.rootContext().setContextProperty("dashboard", dashboard)
    engine.load("main.qml")

    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec())
