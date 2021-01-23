# SoundCloud_playlist
- This script is used to scrape a public playlist.  

- SoundCloud no longer accepts for APP's to be created

## Note

- ChromeDriver versions < 90 are showing the following error:
`
[21012:3780:0122/181236.996:ERROR:device_event_log_impl.cc(211)] [18:12:36.996] USB: usb_device_handle_win.cc:1020 Failed to read descriptor from node connection: A device attached to the system is not functioning. (0x1F)
`
- It doesn't affect the program, but the error is known and  will be fixed in the future.

- More information here:
  - https://stackoverflow.com/questions/64927909/failed-to-read-descriptor-from-node-connection-a-device-attached-to-the-system
  - https://bugs.chromium.org/p/chromium/issues/detail?id=637404#c37
  - https://chromium.googlesource.com/chromium/src.git/+/3182b136ef56eadaf927a2f35446ddb06b133d9e
