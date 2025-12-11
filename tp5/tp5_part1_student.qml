import QtQuick
import QtQuick.Controls
import QtQuick.Dialogs

ApplicationWindow {
    id: root
    width: 400
    height: 800
    visible: true
    title: qsTr("BYAO : Image Gallery")

    // --- image cible pour le FileDialog (sera monImage1, monImage2 ou monImage3) ---
    property Image imageToChange: null

    // --- Boîte de dialogue pour choisir une image ---
    FileDialog {
        id: maBoiteDeDialogue
        title: "Choisissez une image"
        nameFilters: ["Images (*.png *.jpg *.jpeg *.bmp)"]

        onAccepted: {
            if (imageToChange) {
                // En Qt 6, selectedFile est l'URL du fichier choisi
                imageToChange.source = selectedFile
            }
        }
    }

    // ----- Titre en haut -----
    Text {
        id: titre
        text: "BYAO : Image Gallery"
        color: "red"
        font.pointSize: 20
        font.bold: true
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.top: parent.top
        anchors.topMargin: 20
    }

    // ----- Gestionnaire de géométrie : Column -----
    Column {
        id: colonnePrincipale
        spacing: 20
        anchors.top: titre.bottom       // la colonne commence sous le texte
        anchors.topMargin: 20
        anchors.horizontalCenter: parent.horizontalCenter

        // ========== Rectangle 1 ==========
        Rectangle {
            id: rectangle1
            width: 300
            height: 200
            color: "lightgray"

            Text {
                id: texte1
                text: "Image 1"
                color: "white"
                font.pixelSize: 16
                anchors.horizontalCenter: parent.horizontalCenter
                anchors.top: parent.top
                anchors.topMargin: 5
            }

            Image {
                id: monImage1
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.bottom: parent.bottom
                anchors.top: texte1.bottom
                anchors.topMargin: 5
                source: "img/img1.jpg"          // 🔁 adapte le chemin
                fillMode: Image.PreserveAspectCrop
                opacity: 1.0
            }

            // Effet : survol = opacité / 2, retour après A + sortie
            MouseArea {
                id: zone1
                anchors.fill: parent
                hoverEnabled: true
                focus: true
                property bool canReset: false

                onEntered: {
                    monImage1.opacity = 0.5
                    canReset = false
                }

                onExited: {
                    if (canReset) {
                        monImage1.opacity = 1.0
                    }
                }

                Keys.onPressed: (event) => {
                    if (event.key === Qt.Key_A) {
                        canReset = true
                        event.accepted = true
                    }
                }
            }
        }

        // ========== Bouton entre les rectangles ==========
        Button {
            id: monBouton
            text: "Change Image 1"
            anchors.horizontalCenter: parent.horizontalCenter

            // 1er mode : clic sur le bouton -> change monImage1
            onClicked: {
                imageToChange = monImage1
                maBoiteDeDialogue.open()
            }
        }

        // ========== Rectangle 2 ==========
        Rectangle {
            id: rectangle2
            width: 300
            height: 200
            color: "lightgray"

            Text {
                id: texte2
                text: "Image 2"
                color: "white"
                font.pixelSize: 16
                anchors.horizontalCenter: parent.horizontalCenter
                anchors.top: parent.top
                anchors.topMargin: 5
            }

            Image {
                id: monImage2
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.bottom: parent.bottom
                anchors.top: texte2.bottom
                anchors.topMargin: 5
                source: "img/img2.jpg"          // 🔁 adapte le chemin
                fillMode: Image.PreserveAspectCrop
                opacity: 1.0
            }

            // 2e mode : clic direct sur le rectangle -> change monImage2
            MouseArea {
                anchors.fill: parent
                onClicked: {
                    imageToChange = monImage2
                    maBoiteDeDialogue.open()
                }
            }
        }

        // ========== Composant 3 : Flickable scrollable ==========
        Flickable {
            id: flickImg3
            width: 300
            height: 200

            // Taille du contenu scrollable
            contentWidth: width
            contentHeight: height * 3    // contenu plus grand -> scroll possible

            clip: true    // on cache ce qui déborde

            Rectangle {
                id: fond3
                width: flickImg3.width
                height: flickImg3.contentHeight
                color: "lightgray"

                Text {
                    id: texte3
                    text: "Image 3"
                    color: "white"
                    font.pixelSize: 16
                    anchors.horizontalCenter: parent.horizontalCenter
                    anchors.top: parent.top
                    anchors.topMargin: 5
                }

                Image {
                    id: monImage3
                    anchors.top: texte3.bottom
                    anchors.horizontalCenter: parent.horizontalCenter
                    anchors.topMargin: 10
                    width: parent.width
                    height: parent.height - 30     // grande image qui déborde
                    source: "img/img3.jpg"       // 🔁 adapte le chemin
                    fillMode: Image.PreserveAspectCrop
                }

                // 3e mode : appui long -> change monImage3
                MouseArea {
                    anchors.fill: parent

                    onPressAndHold: {
                        imageToChange = monImage3
                        maBoiteDeDialogue.open()
                    }
                }
            }
        }
    }
}
