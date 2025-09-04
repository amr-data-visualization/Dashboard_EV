import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Window {
    visible: true
    width: 1200
    height: 700
    title: "EV Dashboard"

    Rectangle {
        anchors.fill: parent
        color: "#0f172a"   // dark background

        // Top Bar
        RowLayout {
            anchors.top: parent.top
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.margins: 20
            spacing: 20

            Text {
                text: dashboard.date
                color: "white"
                font.pixelSize: 22
            }
            Item { Layout.fillWidth: true }  // pushes time to right
            Text {
                text: dashboard.time
                color: "white"
                font.pixelSize: 22
            }
        }

        // Center Layout
        RowLayout {
            anchors.centerIn: parent
            spacing: 80

            // Speedometer Section
            ColumnLayout {
                spacing: 10
                Layout.alignment: Qt.AlignHCenter

                Text {
                    text: "Speed"
                    color: "white"
                    font.pixelSize: 22
                    horizontalAlignment: Text.AlignHCenter
                }

                Canvas {
                    id: speedGauge
                    width: 260; height: 260
                    onPaint: {
                        var ctx = getContext("2d")
                        ctx.reset()
                        var cx = width/2, cy = height/2
                        var radius = 110
                        var maxSpeed = 50.0   // buggy max speed

                        // background arc
                        ctx.beginPath()
                        ctx.arc(cx, cy, radius, Math.PI*0.75, Math.PI*2.25)
                        ctx.lineWidth = 20
                        ctx.strokeStyle = "#334155"
                        ctx.stroke()

                        // progress arc
                        var angle = (dashboard.speed / maxSpeed) * (Math.PI*1.5)
                        ctx.beginPath()
                        ctx.arc(cx, cy, radius, Math.PI*0.75, Math.PI*0.75 + angle)
                        ctx.lineWidth = 20
                        ctx.strokeStyle = "#22d3ee"
                        ctx.stroke()

                        // needle
                        ctx.beginPath()
                        ctx.moveTo(cx, cy)
                        var nx = cx + radius*Math.cos(Math.PI*0.75 + angle)
                        var ny = cy + radius*Math.sin(Math.PI*0.75 + angle)
                        ctx.lineTo(nx, ny)
                        ctx.lineWidth = 5
                        ctx.strokeStyle = "#f87171"
                        ctx.stroke()
                    }
                    Connections { target: dashboard; function onSpeedChanged() { speedGauge.requestPaint() } }
                }

                Text {
                    text: Math.round(dashboard.speed) + " km/h"
                    font.pixelSize: 26
                    color: "white"
                    horizontalAlignment: Text.AlignHCenter
                    Layout.alignment: Qt.AlignHCenter
                }
            }

            // Status Section
            ColumnLayout {
                spacing: 20

                // Drive Mode
                Column {
                    spacing: 4
                    Text { text: "Drive Mode"; color: "white"; font.pixelSize: 18 }
                    Rectangle {
                        width: 180; height: 60; radius: 10
                        color: "#22c55e"
                        Text { anchors.centerIn: parent; text: dashboard.driveMode; color: "white"; font.pixelSize: 20 }
                    }
                }

                // DBW
                Column {
                    spacing: 4
                    Text { text: "DBW"; color: "white"; font.pixelSize: 18 }
                    Rectangle {
                        width: 180; height: 60; radius: 10
                        color: dashboard.dbw === "Engaged" ? "#16a34a" : "#dc2626"
                        Text { anchors.centerIn: parent; text: dashboard.dbw; color: "white"; font.pixelSize: 20 }
                    }
                }

                // Brake
                Column {
                    spacing: 4
                    Text { text: "Brake"; color: "white"; font.pixelSize: 18 }
                    Rectangle {
                        width: 180; height: 60; radius: 10
                        color: dashboard.brake === "Engaged" ? "#eab308" : "#475569"
                        Text { anchors.centerIn: parent; text: dashboard.brake; color: "white"; font.pixelSize: 20 }
                    }
                }

                // AutoPark
                Column {
                    spacing: 4
                    Text { text: "AutoPark"; color: "white"; font.pixelSize: 18 }
                    Rectangle {
                        width: 180; height: 60; radius: 10
                        color: dashboard.autopark === "Engaged" ? "#3b82f6" : "#64748b"
                        Text { anchors.centerIn: parent; text: dashboard.autopark; color: "white"; font.pixelSize: 20 }
                    }
                }

                // Emergency
                Column {
                    spacing: 4
                    Text { text: "Emergency"; color: "white"; font.pixelSize: 18 }
                    Rectangle {
                        width: 180; height: 60; radius: 10
                        color: dashboard.emergency === "Engaged" ? "#ef4444" : "#64748b"
                        Text { anchors.centerIn: parent; text: dashboard.emergency; color: "white"; font.pixelSize: 20 }
                    }
                }

                // Battery
                Column {
                    spacing: 4
                    Text { text: "Battery"; color: "white"; font.pixelSize: 18 }
                    Rectangle {
                        width: 180; height: 60; radius: 10
                        color: "#facc15"
                        Text { anchors.centerIn: parent; text: dashboard.battery + " %"; color: "black"; font.pixelSize: 20 }
                    }
                }
            }
        }
    }
}
