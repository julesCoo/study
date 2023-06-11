# -*- coding: utf-8 -*-
"""
File: labels.py
Author: Daniel Ebert
Date: 11.06.2023

Description:
    This file contains classes that manage the labels added to the animation.
    They are extracted from animation.py to make the animation code more readable.
"""

from datetime import datetime, timedelta
from matplotlib.animation import FuncAnimation
from matplotlib.artist import Artist
import matplotlib.pyplot as plt


class FrameLabel:
    def __init__(self, keyframes: list[float]):
        self.keyframes = keyframes
        self.frame_label = None

    def setup_animation(self, ax: plt.Axes) -> None:
        self.frame_label = ax.text(
            0.01,
            0.02,
            "",
            horizontalalignment="left",
            verticalalignment="bottom",
            transform=ax.transAxes,
            fontsize=12,
            fontweight="bold",
            color="white",
            bbox=dict(facecolor="black", alpha=0.5, pad=5),
        )

    def update(self, frame: int) -> list[Artist]:
        self.frame_label.set_text(f"{frame}/{len(self.keyframes)}")
        return [self.frame_label]


class TimeLabel:
    def __init__(self, date: datetime, keyframes: list[float]):
        self.date = date
        self.keyframes = keyframes
        self.time_label = None

    def setup_animation(self, ax: plt.Axes) -> None:
        self.time_label = ax.text(
            0.01,
            0.98,
            "",
            horizontalalignment="left",
            verticalalignment="top",
            transform=ax.transAxes,
            fontsize=12,
            fontweight="bold",
            color="white",
            bbox=dict(facecolor="black", alpha=0.5, pad=5),
        )

    def update(self, frame: int) -> list[Artist]:
        dt = self.date + timedelta(hours=self.keyframes[frame])
        self.time_label.set_text(f"{dt.strftime('%Y-%m-%d %H:%M')}")
        return [self.time_label]


class Legend:
    def setup_animation(self, ax):
        handles, labels = ax.get_legend_handles_labels()
        # Remove duplicate labels
        unique_labels = []
        unique_handles = []
        for handle, label in zip(handles, labels):
            if label not in unique_labels:
                unique_labels.append(label)
                unique_handles.append(handle)

        ax.legend(
            unique_handles,
            unique_labels,
            loc="upper right",
            bbox_to_anchor=(1, 1),
            bbox_transform=ax.transAxes,
            labelcolor="white",
            facecolor="black",
        )
