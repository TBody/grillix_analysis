import inspect

def SourcePrint(input_string=""):
  callerframerecord = inspect.stack()[1]    # 0 represents this line
                                            # 1 represents line at caller
  frame = callerframerecord[0]
  info = inspect.getframeinfo(frame)

  print(f"{info.filename}, {info.function}, {info.lineno}: {input_string}")