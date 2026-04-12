"""
Robustness Visualizations

Copyright (c) 2024-2026 AEVA Development Team. All rights reserved.
Open Source with Attribution Required | GitHub: https://github.com/liqcui/AEVA-P
Project ID: AEVA-2026-LQC-dc68e33
"""
import matplotlib.pyplot as plt
import numpy as np

def plot_adversarial_examples(original, adversarial, save_path=None):
    """Plot original vs adversarial"""
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    axes[0].set_title("Original")
    axes[1].set_title("Adversarial")
    if save_path:
        plt.savefig(save_path)
    return fig

def plot_perturbation(perturbation, save_path=None):
    """Plot perturbation"""
    fig = plt.figure(figsize=(8, 6))
    plt.title("Perturbation")
    if save_path:
        plt.savefig(save_path)
    return fig

def plot_robustness_curve(epsilons, accuracies, save_path=None):
    """Plot robustness curve"""
    fig = plt.figure(figsize=(8, 6))
    plt.plot(epsilons, accuracies)
    plt.xlabel("Epsilon")
    plt.ylabel("Accuracy")
    if save_path:
        plt.savefig(save_path)
    return fig
