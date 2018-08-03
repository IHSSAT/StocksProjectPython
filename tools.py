# Indicators like ATR, SMA, RSI, etc. Look for on internet before writing own.
# These will be made for pandas. Convert rest of program to pandas. Check back for more.
# https://github.com/bukosabino/ta/blob/master/ta/trend.py


# Trend Indicators
import pandas as pd
import numpy as np
from math import sqrt

def stddev(lst):
    """returns the standard deviation of lst"""
    final = 0
    for element in lst:
        final = final + element
    mn = final / len(lst)
    variance = sum([(e - mn) ** 2 for e in lst]) / len(lst)
    return sqrt(variance)

def macd(close, n_fast=12, n_slow=26, fillna=False):
    """Moving Average Convergence Divergence (MACD)
    Is a trend-following momentum indicator that shows the relationship between
    two moving averages of prices.
    https://en.wikipedia.org/wiki/MACD
    Args:
        close(pandas.Series): dataset 'Close' column.
        n_fast(int): n period short-term.
        n_slow(int): n period long-term.
        fillna(bool): if True, fill nan values.
    Returns:
        pandas.Series: New feature generated.
    """
    emafast = close.ewm(n_fast).mean()
    emaslow = close.ewm(n_slow).mean()
    macd = emafast - emaslow
    if fillna:
        macd = macd.fillna(0)
    return pd.Series(macd, name='MACD_%d_%d' % (n_fast, n_slow))


def macd_signal(close, n_fast=12, n_slow=26, n_sign=9, fillna=False):
    """Moving Average Convergence Divergence (MACD Signal)
    Shows EMA of MACD.
    https://en.wikipedia.org/wiki/MACD
    Args:
        close(pandas.Series): dataset 'Close' column.
        n_fast(int): n period short-term.
        n_slow(int): n period long-term.
        n_sign(int): n period to signal.
        fillna(bool): if True, fill nan values.
    Returns:
        pandas.Series: New feature generated.
    """
    emafast = close.ewm(n_fast).mean()
    emaslow = close.ewm(n_slow).mean()
    macd = emafast - emaslow
    macd_signal = macd.ewm(n_sign).mean()
    if fillna:
        macd_signal = macd_signal.fillna(0)
    return pd.Series(macd_signal, name='MACD_sign')


def macd_diff(close, n_fast=12, n_slow=26, n_sign=9, fillna=False):
    """Moving Average Convergence Divergence (MACD Diff)
    Shows the relationship between MACD and MACD Signal.
    https://en.wikipedia.org/wiki/MACD
    Args:
        close(pandas.Series): dataset 'Close' column.
        n_fast(int): n period short-term.
        n_slow(int): n period long-term.
        n_sign(int): n period to signal.
        fillna(bool): if True, fill nan values.
    Returns:
        pandas.Series: New feature generated.
    """
    emafast = close.ewm(n_fast).mean()
    emaslow = close.ewm(n_slow).mean()
    macd = emafast - emaslow
    macdsign = macd.ewm(n_sign).mean()
    macd_diff = macd - macdsign
    if fillna:
        macd_diff = macd_diff.fillna(0)
    return pd.Series(macd_diff, name='MACD_diff')


def ema(close, n_fast=12, fillna=False):
    """EMA
    Short Period Exponential Moving Average
    Args:
        close(pandas.Series): dataset 'Close' column.
        n_fast(int): n period short-term.
        fillna(bool): if True, fill nan values.
    Returns:
        pandas.Series: New feature generated.
    """
    emafast = close.ewm(n_fast).mean()
    if fillna:
        emafast = emafast.fillna(method='backfill')
    return pd.Series(emafast, name='ema')


def adx(high, low, close, n=14, fillna=False):
    """Average Directional Movement Index (ADX)Positive and negative directional movement
    form the backbone of the Directional Movement System. Wilder determined directional
    movement by comparing the difference between two consecutive lows 
    with the difference between their respective highs.
    The Plus Directional Indicator (+DI) and Minus Directional Indicator (-DI)
    are derived from smoothed averages of these differences, and measure trend
    direction over time. These two indicators are often referred to collectively
    as the Directional Movement Indicator (DMI).
    The Average Directional Index (ADX) is in turn derived from the smoothed
    averages of the difference between +DI and -DI, and measures the strength
    of the trend (regardless of direction) over time.
    Using these three indicators together, chartists can determine both the
    direction and strength of the trend.
    http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:average_directional_index_adx
    Args:
        high(pandas.Series): dataset 'High' column.
        low(pandas.Series): dataset 'Low' column.
        close(pandas.Series): dataset 'Close' column.
        n(int): n period.
        fillna(bool): if True, fill nan values.
    Returns:
        pandas.Series: New feature generated.
    """
    cs = close.shift(1)

    tr = high.combine(cs, max) - low.combine(cs, min)
    trs = tr.rolling(n).sum()

    up = high - high.shift(1)
    dn = low.shift(1) - low

    pos = ((up > dn) & (up > 0)) * up
    neg = ((dn > up) & (dn > 0)) * dn

    dip = 100 * pos.rolling(n).sum() / trs
    din = 100 * neg.rolling(n).sum() / trs

    dx = 100 * np.abs((dip - din) / (dip + din))
    adx = dx.ewm(n).mean()

    if fillna:
        adx = adx.fillna(40)
    return pd.Series(adx, name='adx')


def adx_pos(high, low, close, n=14, fillna=False):
    """Average Directional Movement Index Positive (ADX)
    The Plus Directional Indicator (+DI) and Minus Directional Indicator (-DI)
    are derived from smoothed averages of these differences, and measure trend
    direction over time. These two indicators are often referred to collectively
    as the Directional Movement Indicator (DMI).
    The Average Directional Index (ADX) is in turn derived from the smoothed
    averages of the difference between +DI and -DI, and measures the strength
    of the trend (regardless of direction) over time.
    Using these three indicators together, chartists can determine both the
    direction and strength of the trend.
    http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:average_directional_index_adx
    Args:
        high(pandas.Series): dataset 'High' column.
        low(pandas.Series): dataset 'Low' column.
        close(pandas.Series): dataset 'Close' column.
        n(int): n period.
        fillna(bool): if True, fill nan values.
    Returns:
        pandas.Series: New feature generated.
    """
    cs = close.shift(1)

    tr = high.combine(cs, max) - low.combine(cs, min)
    trs = tr.rolling(n).sum()

    up = high - high.shift(1)
    dn = low.shift(1) - low

    pos = ((up > dn) & (up > 0)) * up
    neg = ((dn > up) & (dn > 0)) * dn

    dip = 100 * pos.rolling(n).sum() / trs

    if fillna:
        dip = dip.fillna(20)
    return pd.Series(dip, name='adx_pos')


def adx_neg(high, low, close, n=14, fillna=False):
    """Average Directional Movement Index Negative (ADX)
    The Plus Directional Indicator (+DI) and Minus Directional Indicator (-DI)
    are derived from smoothed averages of these differences, and measure trend
    direction over time. These two indicators are often referred to collectively
    as the Directional Movement Indicator (DMI).
    The Average Directional Index (ADX) is in turn derived from the smoothed
    averages of the difference between +DI and -DI, and measures the strength
    of the trend (regardless of direction) over time.
    Using these three indicators together, chartists can determine both the
    direction and strength of the trend.
    http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:average_directional_index_adx
    Args:
        high(pandas.Series): dataset 'High' column.
        low(pandas.Series): dataset 'Low' column.
        close(pandas.Series): dataset 'Close' column.
        n(int): n period.
        fillna(bool): if True, fill nan values.
    Returns:
        pandas.Series: New feature generated.
    """
    cs = close.shift(1)

    tr = high.combine(cs, max) - low.combine(cs, min)
    trs = tr.rolling(n).sum()

    up = high - high.shift(1)
    dn = low.shift(1) - low

    pos = ((up > dn) & (up > 0)) * up
    neg = ((dn > up) & (dn > 0)) * dn

    din = 100 * neg.rolling(n).sum() / trs

    if fillna:
        din = din.fillna(20)
    return pd.Series(din, name='adx_neg')


def adx_indicator(high, low, close, n=14, fillna=False):
    """Average Directional Movement Index Indicator (ADX)
    Returns 1, if Plus Directional Indicator (+DI) is higher than Minus
    Directional Indicator (-DI). Else, return 0.
    http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:average_directional_index_adx
    Args:
        high(pandas.Series): dataset 'High' column.
        low(pandas.Series): dataset 'Low' column.
        close(pandas.Series): dataset 'Close' column.
        n(int): n period.
        fillna(bool): if True, fill nan values.
    Returns:
        pandas.Series: New feature generated.
    """
    cs = close.shift(1)

    tr = high.combine(cs, max) - low.combine(cs, min)
    trs = tr.rolling(n).sum()

    up = high - high.shift(1)
    dn = low.shift(1) - low

    pos = ((up > dn) & (up > 0)) * up
    neg = ((dn > up) & (dn > 0)) * dn

    dip = 100 * pos.rolling(n).sum() / trs
    din = 100 * neg.rolling(n).sum() / trs

    adx_diff = dip - din

    # prepare indicator
    df = pd.DataFrame([adx_diff]).T
    df.columns = ['adx_diff']
    df['adx_ind'] = 0
    df.loc[df['adx_diff'] > 0, 'adx_ind'] = 1
    adx_ind = df['adx_ind']

    if fillna:
        adx_ind = adx_ind.fillna(0)
    return pd.Series(adx_ind, name='adx_ind')


def vortex_indicator_pos(high, low, close, n=14, fillna=False):
    """Vortex Indicator (VI)
    It consists of two oscillators that capture positive and negative trend
    movement. A bullish signal triggers when the positive trend indicator
    crosses above the negative trend indicator or a key level.
    http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:vortex_indicator
    Args:
        high(pandas.Series): dataset 'High' column.
        low(pandas.Series): dataset 'Low' column.
        close(pandas.Series): dataset 'Close' column.
        n(int): n period.
        fillna(bool): if True, fill nan values.
    Returns:
        pandas.Series: New feature generated.
    """
    tr = high.combine(close.shift(1), max) - low.combine(close.shift(1), min)
    trn = tr.rolling(n).sum()

    vmp = np.abs(high - low.shift(1))
    vmm = np.abs(low - high.shift(1))

    vip = vmp.rolling(n).sum() / trn
    if fillna:
        vip = vip.fillna(1)
    return pd.Series(vip, name='vip')


def vortex_indicator_neg(high, low, close, n=14, fillna=False):
    """Vortex Indicator (VI)
    It consists of two oscillators that capture positive and negative trend
    movement. A bearish signal triggers when the negative trend indicator
    crosses above the positive trend indicator or a key level.
    http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:vortex_indicator
    Args:
        high(pandas.Series): dataset 'High' column.
        low(pandas.Series): dataset 'Low' column.
        close(pandas.Series): dataset 'Close' column.
        n(int): n period.
        fillna(bool): if True, fill nan values.
    Returns:
        pandas.Series: New feature generated.
    """
    tr = high.combine(close.shift(1), max) - low.combine(close.shift(1), min)
    trn = tr.rolling(n).sum()

    vmp = np.abs(high - low.shift(1))
    vmm = np.abs(low - high.shift(1))

    vin = vmm.rolling(n).sum() / trn
    if fillna:
        vin = vin.fillna(1)
    return pd.Series(vin, name='vin')


def trix(close, n=15, fillna=False):
    """Trix (TRIX)
    Shows the percent rate of change of a triple exponentially smoothed moving
    average.
    http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:trix
    Args:
        close(pandas.Series): dataset 'Close' column.
        n(int): n period.
        fillna(bool): if True, fill nan values.
    Returns:
        pandas.Series: New feature generated.
    """
    ema1 = close.ewm(span=n, min_periods=n - 1).mean()
    ema2 = ema1.ewm(span=n, min_periods=n - 1).mean()
    ema3 = ema2.ewm(span=n, min_periods=n - 1).mean()
    trix = (ema3 - ema3.shift(1)) / ema3.shift(1)
    trix *= 100
    if fillna:
        trix = trix.fillna(0)
    return pd.Series(trix, name='trix_' + str(n))


def mass_index(high, low, n=9, n2=25, fillna=False):
    """Mass Index (MI)
    It uses the high-low range to identify trend reversals based on range
    expansions. It identifies range bulges that can foreshadow a reversal of the
    current trend.
    http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:mass_index
    Args:
        high(pandas.Series): dataset 'High' column.
        low(pandas.Series): dataset 'Low' column.
        n(int): n low period.
        n2(int): n high period.
        fillna(bool): if True, fill nan values.
    Returns:
        pandas.Series: New feature generated.
    """
    amplitude = high - low
    ema1 = amplitude.ewm(span=n, min_periods=n - 1).mean()
    ema2 = ema1.ewm(span=n, min_periods=n - 1).mean()
    mass = ema1 / ema2
    mass = mass.rolling(n2).sum()
    if fillna:
        mass = mass.fillna(n2)
    return pd.Series(mass, name='mass_index_' + str(n))


def cci(high, low, close, n=20, c=0.015, fillna=False):
    """Commodity Channel Index (CCI)
    CCI measures the difference between a security's price change and its
    average price change. High positive readings indicate that prices are well
    above their average, which is a show of strength. Low negative readings
    indicate that prices are well below their average, which is a show of
    weakness.
    http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:commodity_channel_index_cci
    Args:
        high(pandas.Series): dataset 'High' column.
        low(pandas.Series): dataset 'Low' column.
        close(pandas.Series): dataset 'Close' column.
        n(int): n period.
        c(int): constant.
        fillna(bool): if True, fill nan values.
    Returns:
        pandas.Series: New feature generated.
    """
    pp = (high + low + close) / 3
    cci = (pp - pp.rolling(n).mean()) / pp.rolling(n).std()
    cci = 1 / c * cci
    if fillna:
        cci = cci.fillna(0)
    return pd.Series(cci, name='cci')


def dpo(close, n=20, fillna=False):
    """Detrended Price Oscillator (DPO)
    Is an indicator designed to remove trend from price and make it easier to
    identify cycles.
    http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:detrended_price_osci
    Args:
        close(pandas.Series): dataset 'Close' column.
        n(int): n period.
        fillna(bool): if True, fill nan values.
    Returns:
        pandas.Series: New feature generated.
    """
    dpo = close.shift(int(n / (2 + 1))) - close.rolling(n).mean()
    if fillna:
        dpo = dpo.fillna(0)
    return pd.Series(dpo, name='dpo_' + str(n))


def kst(close, r1=10, r2=15, r3=20, r4=30, n1=10, n2=10, n3=10, n4=15, fillna=False):
    """KST Oscillator (KST)
    It is useful to identify major stock market cycle junctures because its
    formula is weighed to be more greatly influenced by the longer and more
    dominant time spans, in order to better reflect the primary swings of stock
    market cycle.
    https://en.wikipedia.org/wiki/KST_oscillator
    Args:
        close(pandas.Series): dataset 'Close' column.
        r1(int): r1 period.
        r2(int): r2 period.
        r3(int): r3 period.
        r4(int): r4 period.
        n1(int): n1 smoothed period.
        n2(int): n2 smoothed period.
        n3(int): n3 smoothed period.
        n4(int): n4 smoothed period.
        fillna(bool): if True, fill nan values.
    Returns:
        pandas.Series: New feature generated.
    """
    rocma1 = ((close - close.shift(r1)) / close.shift(r1)).rolling(n1).mean()
    rocma2 = ((close - close.shift(r2)) / close.shift(r2)).rolling(n2).mean()
    rocma3 = ((close - close.shift(r3)) / close.shift(r3)).rolling(n3).mean()
    rocma4 = ((close - close.shift(r4)) / close.shift(r4)).rolling(n4).mean()
    kst = 100 * (rocma1 + 2 * rocma2 + 3 * rocma3 + 4 * rocma4)
    if fillna:
        kst = kst.fillna(0)
    return pd.Series(kst, name='kst')


def kst_sig(close, r1=10, r2=15, r3=20, r4=30, n1=10, n2=10, n3=10, n4=15, nsig=9, fillna=False):
    """KST Oscillator (KST Signal)
    It is useful to identify major stock market cycle junctures because its
    formula is weighed to be more greatly influenced by the longer and more
    dominant time spans, in order to better reflect the primary swings of stock
    market cycle.
    http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:know_sure_thing_kst
    Args:
        close(pandas.Series): dataset 'Close' column.
        r1(int): r1 period.
        r2(int): r2 period.
        r3(int): r3 period.
        r4(int): r4 period.
        n1(int): n1 smoothed period.
        n2(int): n2 smoothed period.
        n3(int): n3 smoothed period.
        n4(int): n4 smoothed period.
        nsig(int): n period to signal.
        fillna(bool): if True, fill nan values.
    Returns:
        pandas.Series: New feature generated.
    """
    rocma1 = ((close - close.shift(r1)) / close.shift(r1)).rolling(n1).mean()
    rocma2 = ((close - close.shift(r2)) / close.shift(r2)).rolling(n2).mean()
    rocma3 = ((close - close.shift(r3)) / close.shift(r3)).rolling(n3).mean()
    rocma4 = ((close - close.shift(r4)) / close.shift(r4)).rolling(n4).mean()
    kst = 100 * (rocma1 + 2 * rocma2 + 3 * rocma3 + 4 * rocma4)
    kst_sig = kst.rolling(nsig).mean()
    if fillna:
        kst_sig = kst_sig.fillna(0)
    return pd.Series(kst_sig, name='kst_sig')


def ichimoku_a(high, low, n1=9, n2=26, fillna=False):
    """Ichimoku Kinkō Hyō (Ichimoku)
    It identifies the trend and look for potential signals within that trend.
    http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:ichimoku_cloud
    Args:
        high(pandas.Series): dataset 'High' column.
        low(pandas.Series): dataset 'Low' column.
        n1(int): n1 low period.
        n2(int): n2 medium period.
        fillna(bool): if True, fill nan values.
    Returns:
        pandas.Series: New feature generated.
    """
    conv = (high.rolling(n1).max() + low.rolling(n1).min()) / 2
    base = (high.rolling(n2).max() + low.rolling(n2).min()) / 2

    spana = (conv + base) / 2
    spana = spana.shift(n2)
    if fillna:
        spana = spana.fillna(method='backfill')
    return pd.Series(spana, name='ichimoku_a_' + str(n2))


def ichimoku_b(high, low, n2=26, n3=52, fillna=False):
    """Ichimoku Kinkō Hyō (Ichimoku)
    It identifies the trend and look for potential signals within that trend.
    http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:ichimoku_cloud
    Args:
        high(pandas.Series): dataset 'High' column.
        low(pandas.Series): dataset 'Low' column.
        n2(int): n2 medium period.
        n3(int): n3 high period.
        fillna(bool): if True, fill nan values.
    Returns:
        pandas.Series: New feature generated.
    """
    spanb = (high.rolling(n3).max() + low.rolling(n3).min()) / 2
    spanb = spanb.shift(n2)
    if fillna:
        spanb = spanb.fillna(method='backfill')
    return pd.Series(spanb, name='ichimoku_b_' + str(n2))


# momentum
def rsi(close, n=14, fillna=False):
    """Relative Strength Index (RSI)
    Compares the magnitude of recent gains and losses over a specified time
    period to measure speed and change of price movements of a security. It is
    primarily used to attempt to identify overbought or oversold conditions in
    the trading of an asset.
    https://www.investopedia.com/terms/r/rsi.asp
    Args:
        close(pandas.Series): dataset 'Close' column.
        n(int): n period.
        fillna(bool): if True, fill nan values.
    Returns:
        pandas.Series: New feature generated.
    """
    diff = close.diff()
    which_dn = diff < 0

    up, dn = diff, diff * 0
    up[which_dn], dn[which_dn] = 0, -up[which_dn]

    emaup = up.ewm(n).mean()
    emadn = dn.ewm(n).mean()

    rsi = 100 * emaup / (emaup + emadn)
    if fillna:
        rsi = rsi.fillna(50)
    return pd.Series(rsi, name='rsi')


def money_flow_index(high, low, close, volume, n=14, fillna=False):
    """Money Flow Index (MFI)
    Uses both price and volume to measure buying and selling pressure. It is
    positive when the typical price rises (buying pressure) and negative when
    the typical price declines (selling pressure). A ratio of positive and
    negative money flow is then plugged into an RSI formula to create an
    oscillator that moves between zero and one hundred.
    http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:money_flow_index_mfi
    Args:
        high(pandas.Series): dataset 'High' column.
        low(pandas.Series): dataset 'Low' column.
        close(pandas.Series): dataset 'Close' column.
        volume(pandas.Series): dataset 'Volume' column.
        n(int): n period.
        fillna(bool): if True, fill nan values.
    Returns:
        pandas.Series: New feature generated.
    """
    # 0 Prepare dataframe to work
    df = pd.DataFrame([high, low, close, volume]).T
    df.columns = ['High', 'Low', 'Close', 'Volume']
    df['Up_or_Down'] = 0
    df.loc[(df['Close'] > df['Close'].shift(1)), 'Up_or_Down'] = 1
    df.loc[(df['Close'] < df['Close'].shift(1)), 'Up_or_Down'] = 2

    # 1 typical price
    tp = (df['High'] + df['Low'] + df['Close']) / 3.0

    # 2 money flow
    mf = tp * df['Volume']

    # 3 positive and negative money flow with n periods
    df['1p_Positive_Money_Flow'] = 0.0
    df.loc[df['Up_or_Down'] == 1, '1p_Positive_Money_Flow'] = mf
    n_positive_mf = df['1p_Positive_Money_Flow'].rolling(n).sum()

    df['1p_Negative_Money_Flow'] = 0.0
    df.loc[df['Up_or_Down'] == 2, '1p_Negative_Money_Flow'] = mf
    n_negative_mf = df['1p_Negative_Money_Flow'].rolling(n).sum()

    # 4 money flow index
    mr = n_positive_mf / n_negative_mf
    mr = (100 - (100 / (1 + mr)))
    if fillna:
        mr = mr.fillna(50)
    return pd.Series(mr, name='mfi_' + str(n))


def tsi(close, r=25, s=13, fillna=False):
    """True strength index (TSI)
    Shows both trend direction and overbought/oversold conditions.
    https://en.wikipedia.org/wiki/True_strength_index
    Args:
        close(pandas.Series): dataset 'Close' column.
        r(int): high period.
        s(int): low period.
        fillna(bool): if True, fill nan values.
    Returns:
        pandas.Series: New feature generated.
    """
    m = close - close.shift(1)
    m1 = m.ewm(r).mean().ewm(s).mean()
    m2 = abs(m).ewm(r).mean().ewm(s).mean()
    tsi = m1 / m2
    tsi *= 100
    if fillna:
        tsi = tsi.fillna(0)
    return pd.Series(tsi, name='tsi')


# Volatility
def average_true_range(high, low, close, n=14, fillna=False):
    """Average True Range (ATR)
    The indicator provide an indication of the degree of price volatility.
    Strong moves, in either direction, are often accompanied by large ranges,
    or large True Ranges.
    http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:average_true_range_atr
    Args:
        high(pandas.Series): dataset 'High' column.
        low(pandas.Series): dataset 'Low' column.
        close(pandas.Series): dataset 'Close' column.
        n(int): n period.
    Returns:
        pandas.Series: New feature generated.
    """
    cs = close.shift(1)
    tr = high.combine(cs, max) - low.combine(cs, min)
    tr = tr.ewm(n).mean()
    if fillna:
        tr = tr.fillna(0)
    return pd.Series(tr, name='atr')


def bollinger_mavg(close, n=20, fillna=False):
    """Bollinger Bands (BB)
    N-period simple moving average (MA).
    https://en.wikipedia.org/wiki/Bollinger_Bands
    Args:
        close(pandas.Series): dataset 'Close' column.
        n(int): n period.
    Returns:
        pandas.Series: New feature generated.
    """
    mavg = close.rolling(n).mean()
    if fillna:
        mavg = mavg.fillna(method='backfill')
    return pd.Series(mavg, name='mavg')


def bollinger_hband(close, n=20, ndev=2, fillna=False):
    """Bollinger Bands (BB)
    Upper band at K times an N-period standard deviation above the moving
    average (MA + Kdeviation).
    https://en.wikipedia.org/wiki/Bollinger_Bands
    Args:
        close(pandas.Series): dataset 'Close' column.
        n(int): n period.
        ndev(int): n factor standard deviation
    Returns:
        pandas.Series: New feature generated.
    """
    mavg = close.rolling(n).mean()
    mstd = close.rolling(n).std()
    hband = mavg + ndev * mstd
    if fillna:
        hband = hband.fillna(method='backfill')
    return pd.Series(hband, name='hband')


def bollinger_lband(close, n=20, ndev=2, fillna=False):
    """Bollinger Bands (BB)
    Lower band at K times an N-period standard deviation below the moving
    average (MA − Kdeviation).
    https://en.wikipedia.org/wiki/Bollinger_Bands
    Args:
        close(pandas.Series): dataset 'Close' column.
        n(int): n period.
        ndev(int): n factor standard deviation
    Returns:
        pandas.Series: New feature generated.
    """
    mavg = close.rolling(n).mean()
    mstd = close.rolling(n).std()
    lband = mavg - ndev * mstd
    if fillna:
        lband = lband.fillna(method='backfill')
    return pd.Series(lband, name='lband')


def bollinger_hband_indicator(close, n=20, ndev=2, fillna=False):
    """Bollinger High Band Indicator
    Returns 1, if close is higher than bollinger high band. Else, return 0.
    https://en.wikipedia.org/wiki/Bollinger_Bands
    Args:
        close(pandas.Series): dataset 'Close' column.
        n(int): n period.
        ndev(int): n factor standard deviation
    Returns:
        pandas.Series: New feature generated.
    """
    df = pd.DataFrame([close]).transpose()
    mavg = close.rolling(n).mean()
    mstd = close.rolling(n).std()
    hband = mavg + ndev * mstd
    df['hband'] = 0.0
    df.loc[close > hband, 'hband'] = 1.0
    hband = df['hband']
    if fillna:
        hband = hband.fillna(0)
    return pd.Series(hband, name='bbihband')


def bollinger_lband_indicator(close, n=20, ndev=2, fillna=False):
    """Bollinger Low Band Indicator
    Returns 1, if close is lower than bollinger low band. Else, return 0.
    https://en.wikipedia.org/wiki/Bollinger_Bands
    Args:
        close(pandas.Series): dataset 'Close' column.
        n(int): n period.
        ndev(int): n factor standard deviation
    Returns:
        pandas.Series: New feature generated.
    """
    df = pd.DataFrame([close]).transpose()
    mavg = close.rolling(n).mean()
    mstd = close.rolling(n).std()
    lband = mavg - ndev * mstd
    df['lband'] = 0.0
    df.loc[close < lband, 'lband'] = 1.0
    lband = df['lband']
    if fillna:
        lband = lband.fillna(0)
    return pd.Series(lband, name='bbilband')


def keltner_channel_central(high, low, close, n=10, fillna=False):
    """Keltner channel (KC)
    Showing a simple moving average line (central) of typical price.
    https://en.wikipedia.org/wiki/Keltner_channel
    Args:
        high(pandas.Series): dataset 'High' column.
        low(pandas.Series): dataset 'Low' column.
        close(pandas.Series): dataset 'Close' column.
        n(int): n period.
    Returns:
        pandas.Series: New feature generated.
    """
    tp = (high + low + close) / 3.0
    tp = tp.rolling(n).mean()
    if fillna:
        tp = tp.fillna(method='backfill')
    return pd.Series(tp, name='kc_central')


def keltner_channel_hband(high, low, close, n=10, fillna=False):
    """Keltner channel (KC)
    Showing a simple moving average line (high) of typical price.
    https://en.wikipedia.org/wiki/Keltner_channel
    Args:
        high(pandas.Series): dataset 'High' column.
        low(pandas.Series): dataset 'Low' column.
        close(pandas.Series): dataset 'Close' column.
        n(int): n period.
    Returns:
        pandas.Series: New feature generated.
    """
    tp = ((4 * high) - (2 * low) + close) / 3.0
    tp = tp.rolling(n).mean()
    if fillna:
        tp = tp.fillna(method='backfill')
    return pd.Series(tp, name='kc_hband')


def keltner_channel_lband(high, low, close, n=10, fillna=False):
    """Keltner channel (KC)
    Showing a simple moving average line (low) of typical price.
    https://en.wikipedia.org/wiki/Keltner_channel
    Args:
        high(pandas.Series): dataset 'High' column.
        low(pandas.Series): dataset 'Low' column.
        close(pandas.Series): dataset 'Close' column.
        n(int): n period.
    Returns:
        pandas.Series: New feature generated.
    """
    tp = ((-2 * high) + (4 * low) + close) / 3.0
    tp = tp.rolling(n).mean()
    if fillna:
        tp = tp.fillna(method='backfill')
    return pd.Series(tp, name='kc_lband')


def keltner_channel_hband_indicator(high, low, close, n=10, fillna=False):
    """Keltner Channel High Band Indicator (KC)
    Returns 1, if close is higher than keltner high band channel. Else,
    return 0.
    https://en.wikipedia.org/wiki/Keltner_channel
    Args:
        high(pandas.Series): dataset 'High' column.
        low(pandas.Series): dataset 'Low' column.
        close(pandas.Series): dataset 'Close' column.
        n(int): n period.
    Returns:
        pandas.Series: New feature generated.
    """
    df = pd.DataFrame([close]).transpose()
    df['hband'] = 0.0
    hband = ((4 * high) - (2 * low) + close) / 3.0
    df.loc[close > hband, 'hband'] = 1.0
    hband = df['hband']
    if fillna:
        hband = hband.fillna(0)
    return pd.Series(hband, name='kci_hband')


def keltner_channel_lband_indicator(high, low, close, n=10, fillna=False):
    """Keltner Channel Low Band Indicator (KC)
    Returns 1, if close is lower than keltner low band channel. Else, return 0.
    https://en.wikipedia.org/wiki/Keltner_channel
    Args:
        high(pandas.Series): dataset 'High' column.
        low(pandas.Series): dataset 'Low' column.
        close(pandas.Series): dataset 'Close' column.
        n(int): n period.
    Returns:
        pandas.Series: New feature generated.
    """
    df = pd.DataFrame([close]).transpose()
    df['lband'] = 0.0
    lband = ((-2 * high) + (4 * low) + close) / 3.0
    df.loc[close < lband, 'lband'] = 1.0
    lband = df['lband']
    if fillna:
        lband = lband.fillna(0)
    return pd.Series(lband, name='kci_lband')


def donchian_channel_hband(close, n=20, fillna=False):
    """Donchian channel (DC)
    The upper band marks the highest price of an issue for n periods.
    https://www.investopedia.com/terms/d/donchianchannels.asp
    Args:
        close(pandas.Series): dataset 'Close' column.
        n(int): n period.
    Returns:
        pandas.Series: New feature generated.
    """
    hband = close.rolling(n).max()
    if fillna:
        hband = hband.fillna(method='backfill')
    return pd.Series(hband, name='dchband')


def donchian_channel_lband(close, n=20, fillna=False):
    """Donchian channel (DC)
    The lower band marks the lowest price for n periods.
    https://www.investopedia.com/terms/d/donchianchannels.asp
    Args:
        close(pandas.Series): dataset 'Close' column.
        n(int): n period.
    Returns:
        pandas.Series: New feature generated.
    """
    lband = close.rolling(n).min()
    if fillna:
        lband = lband.fillna(method='backfill')
    return pd.Series(lband, name='dclband')


def donchian_channel_hband_indicator(close, n=20, fillna=False):
    """Donchian High Band Indicator
    Returns 1, if close is higher than donchian high band channel. Else,
    return 0.
    https://www.investopedia.com/terms/d/donchianchannels.asp
    Args:
        close(pandas.Series): dataset 'Close' column.
        n(int): n period.
    Returns:
        pandas.Series: New feature generated.
    """
    df = pd.DataFrame([close]).transpose()
    df['hband'] = 0.0
    hband = close.rolling(n).max()
    df.loc[close >= hband, 'hband'] = 1.0
    hband = df['hband']
    if fillna:
        hband = hband.fillna(0)
    return pd.Series(hband, name='dcihband')


def donchian_channel_lband_indicator(close, n=20, fillna=False):
    """Donchian Low Band Indicator
    Returns 1, if close is lower than donchian low band channel. Else, return 0.
    https://www.investopedia.com/terms/d/donchianchannels.asp
    Args:
        close(pandas.Series): dataset 'Close' column.
        n(int): n period.
    Returns:
        pandas.Series: New feature generated.
    """
    df = pd.DataFrame([close]).transpose()
    df['lband'] = 0.0
    lband = close.rolling(n).min()
    df.loc[close <= lband, 'lband'] = 1.0
    lband = df['lband']
    if fillna:
        lband = lband.fillna(0)
    return pd.Series(lband, name='dcilband')

    # Volume


def acc_dist_index(high, low, close, volume, fillna=False):
    """Accumulation/Distribution Index (ADI)
    Acting as leading indicator of price movements.
    https://en.wikipedia.org/wiki/Accumulation/distribution_index
    Args:
        high(pandas.Series): dataset 'High' column.
        low(pandas.Series): dataset 'Low' column.
        close(pandas.Series): dataset 'Close' column.
        volume(pandas.Series): dataset 'Volume' column.
        fillna(bool): if True, fill nan values.
    Returns:
        pandas.Series: New feature generated.
    """
    clv = ((close - low) - (high - close)) / (high - low)
    clv = clv.fillna(0.0)  # float division by zero
    ad = clv * volume
    ad = ad + ad.shift(1)
    if fillna:
        ad = ad.fillna(0)
    return pd.Series(ad, name='adi')


def on_balance_volume(close, volume, fillna=False):
    """On-balance volume (OBV)
    It relates price and volume in the stock market. OBV is based on a
    cumulative total volume.
    https://en.wikipedia.org/wiki/On-balance_volume
    Args:
        close(pandas.Series): dataset 'Close' column.
        volume(pandas.Series): dataset 'Volume' column.
        fillna(bool): if True, fill nan values.
    Returns:
        pandas.Series: New feature generated.
    """
    df = pd.DataFrame([close, volume]).transpose()
    df['OBV'] = 0
    c1 = close < close.shift(1)
    c2 = close > close.shift(1)
    if c1.any():
        df.loc[c1, 'OBV'] = - volume
    if c2.any():
        df.loc[c2, 'OBV'] = volume
    obv = df['OBV']
    if fillna:
        obv = obv.fillna(0)
    return pd.Series(obv, name='obv')


def on_balance_volume_mean(close, volume, n=10, fillna=False):
    """On-balance volume mean (OBV mean)
    It's based on a cumulative total volume.
    https://en.wikipedia.org/wiki/On-balance_volume
    Args:
        close(pandas.Series): dataset 'Close' column.
        volume(pandas.Series): dataset 'Volume' column.
        n(int): n period.
        fillna(bool): if True, fill nan values.
    Returns:
        pandas.Series: New feature generated.
    """
    df = pd.DataFrame([close, volume]).transpose()
    df['OBV'] = 0
    c1 = close < close.shift(1)
    c2 = close > close.shift(1)
    if c1.any():
        df.loc[c1, 'OBV'] = - volume
    if c2.any():
        df.loc[c2, 'OBV'] = volume
    obv = df['OBV'].rolling(n).mean()
    if fillna:
        obv = obv.fillna(0)
    return pd.Series(obv, name='obv')


def chaikin_money_flow(high, low, close, volume, n=20, fillna=False):
    """Chaikin Money Flow (CMF)
    It measures the amount of Money Flow Volume over a specific period.
    http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:chaikin_money_flow_cmf
    Args:
        high(pandas.Series): dataset 'High' column.
        low(pandas.Series): dataset 'Low' column.
        close(pandas.Series): dataset 'Close' column.
        volume(pandas.Series): dataset 'Volume' column.
        n(int): n period.
        fillna(bool): if True, fill nan values.
    Returns:
        pandas.Series: New feature generated.
    """
    mfv = ((close - low) - (high - close)) / (high - low)
    mfv = mfv.fillna(0.0)  # float division by zero
    mfv *= volume
    cmf = mfv.rolling(n).sum() / volume.rolling(n).sum()
    if fillna:
        cmf = cmf.fillna(0)
    return pd.Series(cmf, name='cmf')


def force_index(close, volume, n=2, fillna=False):
    """Force Index (FI)
    It illustrates how strong the actual buying or selling pressure is. High
    positive values mean there is a strong rising trend, and low values signify
    a strong downward trend.
    http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:force_index
    Args:
        close(pandas.Series): dataset 'Close' column.
        volume(pandas.Series): dataset 'Volume' column.
        n(int): n period.
        fillna(bool): if True, fill nan values.
    Returns:
        pandas.Series: New feature generated.
    """
    fi = close.diff(n) * volume.diff(n)
    if fillna:
        fi = fi.fillna(0)
    return pd.Series(fi, name='fi_' + str(n))


def ease_of_movement(high, low, close, volume, n=20, fillna=False):
    """Ease of movement (EoM, EMV)
    It relate an asset's price change to its volume and is particularly useful
    for assessing the strength of a trend.
    https://en.wikipedia.org/wiki/Ease_of_movement
    Args:
        high(pandas.Series): dataset 'High' column.
        low(pandas.Series): dataset 'Low' column.
        close(pandas.Series): dataset 'Close' column.
        volume(pandas.Series): dataset 'Volume' column.
        n(int): n period.
        fillna(bool): if True, fill nan values.
    Returns:
        pandas.Series: New feature generated.
    """
    emv = (high.diff(1) + low.diff(1)) * (high - low) / (2 * volume)
    emv = emv.rolling(n).mean()
    if fillna:
        emv = emv.fillna(0)
    return pd.Series(emv, name='eom_' + str(n))


def volume_price_trend(close, volume, fillna=False):
    """Volume-price trend (VPT)
    Is based on a running cumulative volume that adds or substracts a multiple
    of the percentage change in share price trend and current volume, depending
    upon the investment's upward or downward movements.
    https://en.wikipedia.org/wiki/Volume%E2%80%93price_trend
    Args:
        close(pandas.Series): dataset 'Close' column.
        volume(pandas.Series): dataset 'Volume' column.
        n(int): n period.
        fillna(bool): if True, fill nan values.
    Returns:
        pandas.Series: New feature generated.
    """
    vpt = volume * ((close - close.shift(1)) / close.shift(1))
    vpt = vpt.shift(1) + vpt
    if fillna:
        vpt = vpt.fillna(0)
    return pd.Series(vpt, name='vpt')

    # Misc...


def daily_return(close, fillna=False):
    """Daily Return (DR)
    Args:
        close(pandas.Series): dataset 'Close' column.
        fillna(bool): if True, fill nan values.
    Returns:
        pandas.Series: New feature generated.
    """
    dr = (close / close.shift(1)) - 1
    dr *= 100
    if fillna:
        dr = dr.fillna(0)
    return pd.Series(dr, name='d_ret')


def cumulative_return(close, fillna=False):
    """Cumulative Return (CR)
    Args:
        close(pandas.Series): dataset 'Close' column.
        fillna(bool): if True, fill nan values.
    Returns:
        pandas.Series: New feature generated.
    """
    cr = (close / close.iloc[0]) - 1
    cr *= 100
    if fillna:
        cr = cr.fillna(method='backfill')
    return pd.Series(cr, name='cum_ret')
