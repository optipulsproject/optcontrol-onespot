gradient_descent = {
        'iter_max': 50,
        'step_init': 2**-25,
        'tolerance': 5*10**-5,
        'step_prediction': False,
        }

# parameters for the bundle of experiments based on zero initial guess
zeroguess = {
    'powers': [1500, 1800, 2100],
    'times': [0.010, 0.015, 0.020],
}

zeroguess['optcontrols'] = [
        f'numericals/zeroguess/{P_YAG}-{T:5.3f}.npy'
        for P_YAG in zeroguess['powers']
        for T in zeroguess['times']
]

zeroguess['reports'] = [
        filename.replace('.npy', '.json')
        for filename in zeroguess['optcontrols']
]

rampdown = {
    'power_max': 2000,
    'power_rampdown': 1500,
    't1': 0.005,
    't2s': [0.005, 0.010],
    'T': 0.012,
}

rampdown['optcontrols'] = [
        'numericals/rampdown/{}-{}-{:5.3f}-{:5.3f}-{:5.3f}.npy'.format(
            rampdown['power_max'],
            rampdown['power_rampdown'],
            rampdown['t1'],
            t2,
            rampdown['T'],
        )
        for t2 in rampdown['t2s']
]

rampdown['reports'] = [
        filename.replace('.npy', '.json')
        for filename in rampdown['optcontrols']
]
