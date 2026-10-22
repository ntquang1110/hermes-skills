# Duration & Convexity calculator — worked-example numbers for fixed-income KF cards.
# Verified 2026-08: 5y 5% coupon bond @ YTM 5% -> Macaulay 4.546y, ModDur 4.3295, Conv 23.936.
# ⚠️ Cash-flow list MUST be [coupon]*(N-1) + [coupon+face]; zipping [coupon]*N + [coupon+face]
#    against range(1,N+1) silently drops the final principal payment (price ~21.6 not 100).
def bond_data(coupon_rate, ytm, years, face=100):
    c = coupon_rate/100*face
    cf = [c]*(years-1) + [c+face]
    t = list(range(1, years+1))
    pv = [ci/(1+ytm/100)**ti for ci, ti in zip(cf, t)]
    price = sum(pv)
    mac = sum(ci*ti/(1+ytm/100)**ti for ci, ti in zip(cf, t)) / price
    mod = mac/(1+ytm/100)
    conv = sum(ci*ti*(ti+1)/(1+ytm/100)**(ti+2) for ci, ti in zip(cf, t)) / price
    return cf, t, pv, price, mac, mod, conv

if __name__ == '__main__':
    years = 5
    cf, t, pv, price, mac, mod, conv = bond_data(5.0, 5.0, years)
    print(f'5y, coupon 5%, YTM 5% -> Price: {price:.4f} (par=100)')
    print(f'Macaulay duration: {mac:.4f} years')
    print(f'Modified duration: {mod:.4f}')
    print(f'Convexity: {conv:.4f}')
    for dy in [0.01, 0.02, -0.01, -0.02]:
        approx_dur = -mod*dy
        approx_conv = approx_dur + 0.5*conv*dy**2
        actual_price = bond_data(5.0, 5.0+dy*100, years)[3]
        actual_pct = (actual_price - price)/price*100
        print(f'dy={dy*100:+.0f}bp: dur-only={approx_dur*100:+.3f}% | dur+conv={approx_conv*100:+.3f}% | actual={actual_pct:+.3f}%')

    # Zero-coupon 5y: Macaulay = exactly maturity
    zprice = 100/(1.05**5)
    print(f'\nZero-coupon 5y: price={zprice:.2f}, Macaulay=5.00, modified={5.0/1.05:.4f}')

    # 10-year comparison + 40/60 portfolio
    cf2, t2, pv2, price2, mac2, mod2, conv2 = bond_data(5.0, 5.0, 10)
    print(f'\n10y, coupon 5%, YTM 5% -> Price: {price2:.4f}, Macaulay: {mac2:.4f}, Modified: {mod2:.4f}, Convexity: {conv2:.4f}')
    w = 0.4
    print(f'Portfolio 40/60: modified duration={w*mod + (1-w)*mod2:.4f}, convexity={w*conv + (1-w)*conv2:.4f}')
