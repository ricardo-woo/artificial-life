import math
import pygame

from settings import (
    COLOR_BORDER,
    COLOR_TEXT_PRIMARY,
    COLOR_LEADERBOARD_TITLE,
    COLOR_OVERLAY,
    COLOR_PROMPT,
    COLOR_TEXT_SECONDARY,
    COLOR_VISION_CIRCLE,
    BORDER_THICKNESS,
    HUD_X_PERCENT,
    HUD_Y_PERCENT,
    HUD_LINE_SPACING,
    HUD_RIGHT_X_PERCENT,
    HUD_RIGHT_Y_PERCENT,
    LEADERBOARD_Y_PERCENT,
    LEADERBOARD_Y_STEP,
)


class UIManager:
    def __init__(self, font):
        self.font = font

    def draw_world_border(
        self,
        screen,
        camera,
        world_width,
        world_height
    ):
        top_left = camera.world_to_screen(0, 0)
        bottom_right = camera.world_to_screen(
            world_width,
            world_height
        )

        world_border = pygame.Rect(
            top_left[0],
            top_left[1],
            bottom_right[0] - top_left[0],
            bottom_right[1] - top_left[1],
        )

        pygame.draw.rect(
            screen,
            COLOR_BORDER,
            world_border,
            BORDER_THICKNESS
        )

    def draw_generation_counter(
        self,
        screen,
        generation_num,
        generation_time
    ):
        gen_text = self.font.render(
            f"Generation: {generation_num}",
            True,
            COLOR_TEXT_PRIMARY
        )

        time_text = self.font.render(
            f"Time: {generation_time:.1f}s",
            True,
            COLOR_TEXT_SECONDARY
        )

        center_x = screen.get_width() // 2

        gen_y = int(screen.get_height() * 0.02)
        time_y = int(screen.get_height() * 0.05)

        screen.blit(
            gen_text,
            (
                center_x - gen_text.get_width() // 2,
                gen_y
            )
        )

        screen.blit(
            time_text,
            (
                center_x - time_text.get_width() // 2,
                time_y
            )
        )

    def draw_leaderboard(
        self,
        screen,
        top_organisms,
        generation_num
    ):
        overlay = pygame.Surface(
            (screen.get_width(), screen.get_height()),
            pygame.SRCALPHA
        )

        overlay.fill(COLOR_OVERLAY)
        screen.blit(overlay, (0, 0))

        title_text = self.font.render(
            f"--- Generation {generation_num} Leaderboard ---",
            True,
            COLOR_LEADERBOARD_TITLE
        )

        screen.blit(
            title_text,
            (
                screen.get_width() // 2
                - title_text.get_width() // 2,
                int(screen.get_height() * 0.10)
            )
        )

        y = int(
            screen.get_height()
            * LEADERBOARD_Y_PERCENT
        )

        for i, org in enumerate(top_organisms[:5], 1):
            text = self.font.render(
                f"{i}. Fitness: {org.fitness:.1f} | "
                f"Food Eaten: {org.food_eaten} | "
                f"Age: {org.age:.1f}",
                True,
                COLOR_TEXT_PRIMARY
            )

            screen.blit(
                text,
                (
                    screen.get_width() // 2
                    - text.get_width() // 2,
                    y
                )
            )

            y += LEADERBOARD_Y_STEP

        prompt_text = self.font.render(
            "Press [ENTER] to start next generation",
            True,
            COLOR_PROMPT
        )

        screen.blit(
            prompt_text,
            (
                screen.get_width() // 2
                - prompt_text.get_width() // 2,
                y + 60
            )
        )

    def draw_selection_and_hud(
        self,
        screen,
        camera,
        selected_organism,
        food_grid
    ):
        if selected_organism is None:
            return

        screen_x, screen_y = camera.world_to_screen(
            selected_organism.x,
            selected_organism.y
        )

        # Vision radius circle
        pygame.draw.circle(
            screen,
            COLOR_VISION_CIRCLE,
            (screen_x, screen_y),
            int(
                selected_organism.vision
                * camera.zoom
            ),
            1,
        )

        brain_inputs = (
            selected_organism.get_brain_inputs(food_grid)
        )

        brain_outputs = (
            selected_organism.brain.predict(
                brain_inputs
            )
        )

        stats = [
            f"Energy: {selected_organism.energy:.1f}",
            f"Speed: {selected_organism.speed:.2f}",
            f"Vision: {selected_organism.vision:.1f}",
            f"Brain Inputs:",
            f"  Energy:     {brain_inputs[0]:.2f}",
            f"  Food?:      {brain_inputs[1]:.1f}",
            f"  Distance:   {brain_inputs[2]:.2f}",
            f"  Angle (sin): {brain_inputs[3]:.2f}",
            f"  Angle (cos): {brain_inputs[4]:.2f}",
            f"  Time Food:  {brain_inputs[5]:.2f}",
            f"  Noise:      {brain_inputs[6]:.2f}",
            f"Brain Outputs:",
            f"  Turn:       {brain_outputs[0]:.2f}",
            f"  Movement:   {brain_outputs[1]:.2f}",
        ]

        x = int(
            screen.get_width()
            * HUD_RIGHT_X_PERCENT
        )

        y = int(
            screen.get_height()
            * HUD_RIGHT_Y_PERCENT
        )

        for stat in stats:
            text = self.font.render(
                stat,
                True,
                COLOR_TEXT_PRIMARY
            )

            screen.blit(
                text,
                (x, y)
            )

            y += HUD_LINE_SPACING

    def draw_live_leaderboard(self,screen,organisms):
        sorted_organisms = sorted(
            organisms,
            key=lambda org: org.fitness,
            reverse=True
        )
        leaderboard_rows = []

        x = int(
            screen.get_width()
            * HUD_X_PERCENT
        )

        y = int(
            screen.get_height()
            * LEADERBOARD_Y_PERCENT
        )

        for i, org in enumerate(
            sorted_organisms[:10],
            1
        ):
            row_rect = pygame.Rect(
                x,
                y,
                400,
                LEADERBOARD_Y_STEP
            )

            text = self.font.render(
                f"{i}.  {org.fitness:.1f}, "
                f"Food: {org.food_eaten}, "
                f"Age: {org.age:.1f}",
                True,
                COLOR_TEXT_PRIMARY
            )

            screen.blit(
                text,
                (x, y)
            )

            leaderboard_rows.append(
                (row_rect, org)
            )

            y += LEADERBOARD_Y_STEP

        return leaderboard_rows

    def draw_debug(self,screen,organisms,foods,generation_num,generation_time,fps
    ):
        debug_info = [
            f"Current Generation: {generation_num}",
            f"Generation Time:    {generation_time:.1f}s",
            f"Food Available:     {len(foods)}",
            f"Organisms Alive:    {len(organisms)}",
            f"FPS:                {fps:.1f}",
        ]

        x = int(
            screen.get_width()
            * HUD_X_PERCENT
        )

        y = int(
            screen.get_height()
            * HUD_Y_PERCENT
        )

        for info in debug_info:
            text = self.font.render(
                info,
                True,
                COLOR_TEXT_PRIMARY
            )

            screen.blit(
                text,
                (x, y)
            )

            y += HUD_LINE_SPACING

        leaderboard_rows = self.draw_live_leaderboard(
            screen,
            organisms
        )

        return leaderboard_rows