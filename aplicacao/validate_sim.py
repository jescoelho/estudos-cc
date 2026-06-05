import numpy as np, json

with open('real_returns.json') as f:
    ret = np.array(json.load(f))

print('=== VALORES DE REFERENCIA (Python) ===')
print(f'N retornos : {len(ret)}')
print()

# --- Historico ---
vp_h = abs(np.percentile(ret, 1.0))
th   = np.percentile(ret, 1.0)
es_h = abs(ret[ret < th].mean())
print(f'[HIST]  VaR 99% = {vp_h*100:.4f}%   ES = {es_h*100:.4f}%')

# --- Parametrico ---
sig  = ret.std(ddof=1)
vp_p = 2.3263 * sig
print(f'[PARAM] VaR 99% = {vp_p*100:.4f}%')

# --- EWMA (replica var_ibovespa.py: sigma2_0=0, inovacao=r[t-1]) ---
s2 = 0.0
for r in ret[:-1]:          # itera ret[0]..ret[n-2], igual ao Python
    s2 = 0.94 * s2 + 0.06 * r**2
vp_e = 2.3263 * np.sqrt(s2)
print(f'[EWMA]  VaR 99% = {vp_e*100:.4f}%  (sigma_ewma={np.sqrt(s2)*100:.4f}%)')

# --- Monte Carlo com Mulberry32 (mesmo algoritmo do JS) ---
def mulberry32(seed):
    s = seed & 0xFFFFFFFF
    while True:
        s = (s + 0x6D2B79F5) & 0xFFFFFFFF
        t = ((s ^ (s >> 15)) * (1 | s)) & 0xFFFFFFFF
        t = (t + ((t ^ (t >> 7)) * (61 | t))) & 0xFFFFFFFF
        yield ((t ^ (t >> 14)) & 0xFFFFFFFF) / 4294967296

def rnorm_bm(rng):
    while True:
        u = next(rng)*2 - 1
        v = next(rng)*2 - 1
        w = u*u + v*v
        if 0 < w < 1:
            return u * np.sqrt(-2 * np.log(w) / w)

N_MC = 1000
SEED = 42
mu_r, sig_r = ret.mean(), ret.std(ddof=1)
rng = mulberry32(SEED)
sim = np.array([mu_r + sig_r * rnorm_bm(rng) for _ in range(N_MC)])
vp_m = abs(np.percentile(sim, 1.0))
th_m = np.percentile(sim, 1.0)
es_m = abs(sim[sim < th_m].mean())
print(f'[MC]    VaR 99% = {vp_m*100:.4f}%   ES = {es_m*100:.4f}%  (seed={SEED}, n={N_MC}, Mulberry32)')

print()
print(f'VaR 10d EWMA = {vp_e*np.sqrt(10)*100:.4f}%')
print()

print('--- Backtesting ---')
win = ret[-250:]
exc = int((np.abs(win) > vp_h).sum())
sem = 'VERDE' if exc <= 4 else 'AMARELO' if exc < 10 else 'VERMELHO'
print(f'Excecoes : {exc}  ({exc/250*100:.2f}%)  Semaforo: {sem}')

print()
print('--- Stress Test (nocional R$10M) ---')
vb_h = vp_h * 10_000_000
for name, r in [('COVID',-0.1207),('Brexit',-0.0736),('Lehman',-0.0992),('Eleicoes',-0.0550),('Hipotetico',-0.2000)]:
    p = abs(r*10_000_000); m = p/vb_h
    print(f'  {name:<12} {r*100:>7.2f}%  R${p:>14,.2f}  {m:.2f}x  {"EXTREMO" if m>=3 else "SEVERO" if m>=1.5 else "MODERADO"}')
