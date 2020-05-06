def check_ffmpeg():
    # If animating, add this near the top of your script. This saves a painful error where the
    # animation routine will crash after performing all of the data processing because it can't
    # find ffmpeg to write a movie file.
    import subprocess
    try:
        check_ffmpeg = subprocess.run(['ffmpeg', '-version'], shell=True, capture_output=True)
        
        # returncode == 1 indicates that the command ran correctly. Otherwise raise error
        if check_ffmpeg.returncode != 1:
            print("FFMPEG ERROR: {}".format(check_ffmpeg.stderr.decode("utf-8")))
            check_ffmpeg.check_returncode()
    except:
        raise RuntimeError("Call to ffmpeg failed. Check that the module is loaded correctly.")