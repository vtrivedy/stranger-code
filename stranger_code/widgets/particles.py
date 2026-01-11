"""Portal particles widget - Upside Down atmospheric effect."""

from __future__ import annotations

import random
from typing import TYPE_CHECKING, Any

from textual.reactive import reactive
from textual.widgets import Static

if TYPE_CHECKING:
    from textual.timer import Timer

# Portal particle characters (floating debris from the Upside Down)
PARTICLES = ["·", "˚", "*", "∙", "°", "•"]

# Dim colors for particles (subtle, atmospheric)
PARTICLE_COLORS = [
    "#3a2020",  # Very dim red
    "#4a2a2a",  # Slightly brighter
    "#2a2a3a",  # Dim blue
    "#3a3a2a",  # Dim yellow
    "#2a3a2a",  # Dim green (rare)
]


class PortalParticle:
    """A single floating particle."""

    def __init__(self, width: int, height: int) -> None:
        """Initialize a particle at a random position."""
        self.x = random.randint(0, max(1, width - 1))
        self.y = random.randint(0, max(1, height - 1))
        self.char = random.choice(PARTICLES)
        self.color = random.choice(PARTICLE_COLORS)
        self.dx = random.choice([-1, 0, 0, 0, 1])  # Slow horizontal drift
        self.dy = random.choice([-1, 0, 0, 1])  # Slow vertical drift
        self.lifetime = random.randint(10, 30)  # Ticks before respawn
        self._width = width
        self._height = height

    def update(self) -> bool:
        """Update particle position. Returns False if particle should respawn."""
        self.lifetime -= 1
        if self.lifetime <= 0:
            return False

        # Move with slight drift
        self.x += self.dx
        self.y += self.dy

        # Wrap around edges
        if self.x < 0:
            self.x = self._width - 1
        elif self.x >= self._width:
            self.x = 0

        if self.y < 0:
            self.y = self._height - 1
        elif self.y >= self._height:
            self.y = 0

        # Random direction changes
        if random.random() < 0.1:
            self.dx = random.choice([-1, 0, 0, 0, 1])
            self.dy = random.choice([-1, 0, 0, 1])

        return True

    def respawn(self, width: int, height: int) -> None:
        """Respawn particle at new random position."""
        self._width = width
        self._height = height
        self.x = random.randint(0, max(1, width - 1))
        self.y = random.randint(0, max(1, height - 1))
        self.char = random.choice(PARTICLES)
        self.color = random.choice(PARTICLE_COLORS)
        self.lifetime = random.randint(10, 30)


class PortalParticles(Static):
    """Floating particles background effect - Upside Down atmosphere."""

    DEFAULT_CSS = """
    PortalParticles {
        width: 100%;
        height: 100%;
        background: transparent;
    }
    """

    active: reactive[bool] = reactive(True)
    _timer: Timer | None = None
    _particles: list[PortalParticle]
    _particle_count: int = 15

    def __init__(self, particle_count: int = 15, **kwargs: Any) -> None:
        """Initialize portal particles.

        Args:
            particle_count: Number of floating particles
            **kwargs: Additional arguments passed to parent
        """
        super().__init__("", **kwargs)
        self._particle_count = particle_count
        self._particles = []

    def on_mount(self) -> None:
        """Start particle animation."""
        self._init_particles()
        if self.active:
            self._start_animation()

    def on_resize(self) -> None:
        """Reinitialize particles when size changes."""
        self._init_particles()

    def _init_particles(self) -> None:
        """Initialize particles based on current size."""
        width = self.size.width
        height = self.size.height
        if width > 0 and height > 0:
            self._particles = [
                PortalParticle(width, height) for _ in range(self._particle_count)
            ]
            self._render_particles()

    def watch_active(self, active: bool) -> None:  # noqa: FBT001
        """Start or stop animation when active changes."""
        if active:
            self._start_animation()
        else:
            self._stop_animation()

    def _start_animation(self) -> None:
        """Start the particle animation."""
        if self._timer is None:
            self._timer = self.set_interval(0.2, self._animate_frame)

    def _stop_animation(self) -> None:
        """Stop the particle animation."""
        if self._timer:
            self._timer.stop()
            self._timer = None
        self.update("")

    def _animate_frame(self) -> None:
        """Advance animation by one frame."""
        width = self.size.width
        height = self.size.height

        if width <= 0 or height <= 0:
            return

        for particle in self._particles:
            if not particle.update():
                particle.respawn(width, height)

        self._render_particles()

    def _render_particles(self) -> None:
        """Render particles to a grid and update display."""
        width = self.size.width
        height = self.size.height

        if width <= 0 or height <= 0:
            return

        # Create grid
        grid = [[" " for _ in range(width)] for _ in range(height)]

        # Place particles
        for particle in self._particles:
            if 0 <= particle.x < width and 0 <= particle.y < height:
                grid[particle.y][particle.x] = f"[{particle.color}]{particle.char}[/{particle.color}]"

        # Render to string
        lines = ["".join(row) for row in grid]
        self.update("\n".join(lines))


class PortalParticlesOverlay(Static):
    """A simpler particle overlay that renders as a single-line decoration."""

    DEFAULT_CSS = """
    PortalParticlesOverlay {
        width: 100%;
        height: 1;
        background: transparent;
        text-align: center;
    }
    """

    active: reactive[bool] = reactive(True)
    _timer: Timer | None = None
    _frame: int = 0

    def on_mount(self) -> None:
        """Start animation."""
        if self.active:
            self._start_animation()
        self._render_frame()

    def watch_active(self, active: bool) -> None:  # noqa: FBT001
        """Start or stop animation."""
        if active:
            self._start_animation()
        else:
            self._stop_animation()

    def _start_animation(self) -> None:
        """Start animation timer."""
        if self._timer is None:
            self._timer = self.set_interval(0.3, self._animate)

    def _stop_animation(self) -> None:
        """Stop animation timer."""
        if self._timer:
            self._timer.stop()
            self._timer = None

    def _animate(self) -> None:
        """Advance frame."""
        self._frame += 1
        self._render_frame()

    def _render_frame(self) -> None:
        """Render the current particle line."""
        width = self.size.width
        if width <= 0:
            width = 60

        # Generate sparse particles
        result = ""
        for i in range(width):
            # Use frame offset for movement effect
            pos = (i + self._frame) % width
            if random.random() < 0.05:  # 5% chance for particle
                char = random.choice(PARTICLES)
                color = random.choice(PARTICLE_COLORS)
                result += f"[{color}]{char}[/{color}]"
            else:
                result += " "

        self.update(result)
