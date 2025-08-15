import numpy as np
import matplotlib.pyplot as plt



def safe_phase(Z, eps=1e-12):
    mag = np.abs(Z)
    return np.where(mag > eps, Z / mag, np.exp(1j * 2 * np.pi * np.random.rand(*Z.shape)))

def make_ground_truth(N=256):

    x = np.linspace(-1, 1, N)
    X, Y = np.meshgrid(x, x)
    img = np.zeros((N, N))

    # Gaussian
    img += np.exp(-((X)**2 + (Y)**2) / 0.02)
    # Ring
    R = np.sqrt(X**2 + Y**2)
    img += np.exp(-((R - 0.3)**2) / 0.001)
    # Rectangle
    img[(np.abs(X) < 0.3) & (np.abs(Y) < 0.05)] += 0.8
    # Disk
    img[(X**2 + Y**2) < 0.05] += 1.0

    img = img / img.max()
    mask = img > 1e-3  

    return img, mask

def make_sampling_mask(N, keep_ratio=0.65, radial_bias=3.0):

    cy, cx = N // 2, N // 2
    Y, X = np.ogrid[:N, :N]
    R = np.sqrt((X - cx) ** 2 + (Y - cy) ** 2)
    R = R / R.max()
    prob = np.exp(-radial_bias * R)
    prob = prob / prob.max() * keep_ratio
    mask = np.random.rand(N, N) < prob
    return mask

def make_measurements(gt_img, freq_mask, noise_std=0.0):
    F_gt = np.fft.fftshift(np.fft.fft2(gt_img))
    mag_gt = np.abs(F_gt)
    mag_meas = np.zeros_like(mag_gt)
    noise = noise_std * np.random.randn(np.count_nonzero(freq_mask))
    mag_meas[freq_mask] = mag_gt[freq_mask] + noise
    mag_meas = np.clip(mag_meas, 0, None)
    return mag_meas, mag_gt

def reconstruct(mag_meas, freq_mask, support_mask, 
                max_iter=300, beta=0.9, switch_hio_at=50, polish_last=50):
    N = mag_meas.shape[0]

    phase_init = np.exp(1j * 2 * np.pi * np.random.rand(N, N))
    F_est = mag_meas * phase_init
    img_est = np.fft.ifft2(np.fft.ifftshift(F_est)).real

    err_curve = []

    for it in range(max_iter):

        F_est = np.fft.fftshift(np.fft.fft2(img_est))
        phase = safe_phase(F_est)
        F_est[freq_mask] = mag_meas[freq_mask] * phase[freq_mask]

        img_back = np.fft.ifft2(np.fft.ifftshift(F_est)).real

        if it < switch_hio_at:
 
            img_back[~support_mask] = 0
            img_back = np.clip(img_back, 0, None)
            img_est = img_back
        else:
 
            mask_out = (~support_mask) | (img_back < 0)
            img_est[mask_out] = img_est[mask_out] - beta * img_back[mask_out]
            img_est[~mask_out] = img_back[~mask_out]

        if it > max_iter - polish_last:
            img_est[~support_mask] = 0
            img_est = np.clip(img_est, 0, None)

        F_check = np.fft.fftshift(np.fft.fft2(img_est))
        err = np.linalg.norm(np.abs(F_check)[freq_mask] - mag_meas[freq_mask]) / np.linalg.norm(mag_meas[freq_mask])
        err_curve.append(err)

    img_est = img_est - img_est.min()
    img_est = img_est / img_est.max()
    return img_est, err_curve

def nrmse(a, b):
    return np.sqrt(np.mean((a - b) ** 2)) / (b.max() - b.min())

def ncc(a, b):
    a_ = a - np.mean(a)
    b_ = b - np.mean(b)
    return np.sum(a_ * b_) / np.sqrt(np.sum(a_**2) * np.sum(b_**2))



if __name__ == "__main__":
    N = 256
    gt_img, support_mask = make_ground_truth(N)
    freq_mask = make_sampling_mask(N, keep_ratio=0.65)
    mag_meas, mag_gt = make_measurements(gt_img, freq_mask, noise_std=0.01)

    recon_img, err_curve = reconstruct(mag_meas, freq_mask, support_mask, max_iter=300)


    print(f"Image NRMSE: {nrmse(recon_img, gt_img):.4f}")
    print(f"Image NCC:   {ncc(recon_img, gt_img):.4f}")


    plt.figure(figsize=(12, 8))
    plt.subplot(2,3,1)
    plt.imshow(gt_img, cmap="gray"); plt.title("Ground Truth")
    plt.subplot(2,3,2)
    plt.imshow(freq_mask, cmap="gray"); plt.title("Freq. Mask")
    plt.subplot(2,3,3)
    plt.imshow(recon_img, cmap="gray"); plt.title("Reconstruction")
    plt.subplot(2,3,4)
    plt.imshow(np.log1p(mag_gt), cmap="magma"); plt.title("Log|FFT| GT")
    plt.subplot(2,3,5)
    plt.imshow(np.log1p(np.abs(np.fft.fftshift(np.fft.fft2(recon_img)))), cmap="magma"); plt.title("Log|FFT| Recon")
    plt.subplot(2,3,6)
    plt.plot(err_curve); plt.title("Fourier Consistency Error")
    plt.tight_layout()
    plt.show()
