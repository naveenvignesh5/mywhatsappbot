### Whatsapp Bot Using Selenium / Python

#### Simple Whatsapp Bot Module to send messages, attachments.

* Based on selenium testing software written on python
* Uses autoit automation tool to send attachments on windows.

#### Command Line Instructions

1. Place the required images files inside Media folder.
2. Update your message.csv to reflect the following format.

```csv
text, some text
image, image.png
image, image1.jpg
text,some text2
```

**(text, image - type of message to be sent)**

3.  Click startbot.command
4.  New browser **window (not tab)** will be opened.
5.  Scan QR Code for whatsapp
6.  Messages will be sent and after being sent browser will close automatically.