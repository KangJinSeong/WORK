import numpy as np

def sine_wave(f,overSampRate,phase,nCy1):
    '''
    Parameters:
    
    f: frequency
    oversamprate: oversampling rate
    phase: desired phase shift in radians
    ncy1: number of cycles of sine wave to gerate
    
    Returns:
    (t,g) :  time base(t) and the signal g(t) as tuple
    
    Example:
    f = 10; oversamprate = 30;
    phase = 1/3*np.pi; nCy1 = 5;
    (t,g) = sine_wave(f,overSampRate,phase,nCy1)
    '''
    
    fs = overSampRate * f # sampling frequency
    t = np.arange(0,nCy1*1/f-1/fs, 1/fs) # time base
    g = np.sin(2*np.pi*f*t+phase) # replace woth cos if a cosine wave is desired
    
    return (t,g)

def square_wave(f,overSampRate,nCy1):
    '''
    Parameters:
    
    f: frequency
    oversamprate: oversampling rate
    ncy1: number of cycles of sine wave to gerate
    
    Returns:
    (t,g) :  time base(t) and the signal g(t) as tuple
    
    Example:
    f = 10; oversamprate = 30; nCy1 = 5

    (t,g) = sqare_wave(f,overSampRate,nCy1)
    '''
    
    fs = overSampRate * f # sampling frequency
    t = np.arange(0,nCy1*1/f-1/fs, 1/fs) # time base
    g = np.sign(np.sin(2*np.pi*f*t)) # replace woth cos if a cosine wave is desired
    
    return (t,g)

def rect_pulse(A,Fs,T):
    '''
    Generate isolated rectangular pulse with the following parameters
    
    Parameters:
    A: amplitude of the rectangular pulse
    fs : sampling frequency in Hz
    T : duration of the pulse in seconds
    
    Returns:
    (t,g) :  time base(t) and the signal g(t) as tuple
    
    Example:
    A = 1; fs = 500; T = 0.2;
    (t,g) = rect_pulse(A,fs,T)
    '''
    t = np.arange(-0.5,0.5,1/Fs)
    rect = (t>-T/2)*(t<T/2) + 0.5*(t==T/2) + 0.5*(t==-T/2)
    g = A*rect
    return(t,g)


def gaussian_pulse(Fs,sigma):
    '''
    Generate isolated Gaussian pulse with the following parameters
    
    Parameters:
    fs : sampling frequency in Hz
    sigma : pulse width in seconds
    
    Returns:
    (t,g) :  time base(t) and the signal g(t) as tuple
    
    Example:
    fs = 80; sigma = 0.1;
    (t,g) = gaussian_pulse(Fs,sigma)
    '''
    t = np.arange(-0.5,0.5,1/Fs)
    g = 1/(np.sqrt(2*np.pi)*sigma)*(np.exp(-t**2/(2*sigma**2)))
    return(t,g)
