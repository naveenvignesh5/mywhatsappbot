### Whatsapp Bot Using Selenium / Python

#### Simple Whatsapp Bot Module to send messages, attachments.

- Based on selenium testing software written on python

#### Command Line Instructions

1. Place the required images files inside `/Media/` folder.
2. Update your message.csv to reflect the following format.

```csv
text, some text
image, image.png
image, image1.jpg
text,some text2
video,video1.mp4
video,apple_video.mov
```

3. Update your contacts.csv to reflect the following format.

```csv
contact_name,contact_number
```

**Notes:**

- `contact_name` must be the same as the name in your phone contacts.

  **Eg:**

    ```csv
    john_doe_work1,9876543210
    jane_doe_1,1234567890
    ```

- **(text, image, video)** - type of message to be sent

### Instuctions to use

1.  Click **startbot.command**
2.  **New browser window** will be opened.
3.  Scan **QR Code** for whatsapp
4.  Messages will be sent and after being sent browser will close automatically.

### Generate Windows Executable

```shell
$ python setup_win.py build
```
