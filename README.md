# How to take pictures using Ras Pi with libcamera

Libcamera is a support library for Linux, Android and ChromeOS which was introduced to the Raspberry Pi via a previous Raspberry Pi OS, but it has come into the spotlight due to the changes made for Bullseye. The app offers an easy to use series of tools which can tweak many different camera settings (aperture, color balance, exposure) via a series of switches issued when the command is invoked¹.

## Connecting and Configuring the Camera

For getting images with Raspberry Pi, `Legacy Camera Support` must be disabled. Although it is the default in Raspberry Pi OS 'Bullseyebut' if you get an error when using `libcamera` you can try turning it off.

## Taking Still Images

The first step in any coding project is “Hello World”, and libcamera comes with its own in the form of `libcamera-hello`. We will use this command to ensure that our camera is working.

1. Open a terminal and enter the command to start the camera. A preview window will appear for five seconds, before closing.

```
libcamera-hello
```

2. Run the command again, but this time we shall use a switch (argument) to force the preview window to stay open. To close the window click on the X, or press CTRL + C. Using the preview window in this manner gives Raspberry Pi HQ camera users plenty of time to tweak the aperture and focus of the lens before taking any images.

```
libcamera-hello -t 0
```

The camera works but how do we capture an image? To quickly capture an image we can use `libcamera-jpeg`. This tool is a simple “point and shoot” camera.

3. Open a terminal and enter the command to start the camera, take a picture and save it as test.jpg.

```
libcamera-jpeg -o test.jpg
```

4. Use the following options to take a picture, called test1080.jpg with a preview delay of five seconds, and an image size of 1920 x 1080. Note that the time -t is specified in milliseconds.

```
libcamera-jpeg -o test1080.jpg -t 5000 --width 1920 --height 1080
```

## Advanced Options

The more advanced way to capture images is via `libcamera-still`. This command shares a similarity to raspistill, in that many of the same arguments work across the pair.

1. Open a terminal and enter the command to start the camera, take a picture and save it as still-test.jpg.

```
libcamera-still -o still-test.jpg
```

2. To capture a png image, use the -e switch to specify the encoding and ensure the filename ends in .png.

```
libcamera-still -o still-test.png -e png
```

3. To disable the preview window of libcamera, you can use the `-n` switch³.

```
libcamera-still -o still-test.jpg -n
```

## How to get the complete list of settings for libcamera?

To get more information about libcamera commands and options, you can use `--help` after any command, for example:

```
libcamera-jpeg --help
libcamera-still --help
libcamera-hello --help
```

This will show you all the possible switches and arguments you can use with each command.

## Conclusion

In this markdown file, we have learned how to take pictures using Ras Pi with libcamera. We have seen how to connect and configure the camera, how to use different commands and options to capture images, and how to get more information about libcamera. Libcamera is a powerful and flexible tool that can help you create amazing projects with vision on your Raspberry Pi.
