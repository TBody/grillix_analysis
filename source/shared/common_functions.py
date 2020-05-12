def smoothstep(x0, x, wx, order=3):
    # x0 = centre
    # x = position where to evaluate
    # wx = width

    xn  = (x - x0) / wx + 0.5

    xn[xn<=0] = 0
    xn[xn>=1] = 1
    
    if order == 1:
        return xn
    elif order == 2:
        return -2.0   * xn**3  + 3.0    * xn**2
    elif order == 3:
        return 6.0    * xn**5  - 15.0   * xn**4  + 10.0    * xn**3
    elif order == 4:
        return -20.0  * xn**7  + 70.0   * xn**6  - 84.0    * xn**5  + 35.0    * xn**4
    elif order == 5:
        return 70.0   * xn**9  - 315.0  * xn**8  + 540.0   * xn**7  - 420.0   * xn**6  + 126.0   * xn**5
    elif order == 6:
        return -252.0 * xn**11 + 1386.0 * xn**10 - 3080.0  * xn**9  + 3465.0  * xn**8  - 1980.0  * xn**7  + 462.0  * xn**6
    elif order == 7:
        return 924.0  * xn**13 - 6006.0 * xn**12 + 16380.0 * xn**11 - 24024.0 * xn**10 + 20020.0 * xn**9  - 9009.0 * xn**8 + 1716.0 * xn**7
    else:
        return NotImplemented