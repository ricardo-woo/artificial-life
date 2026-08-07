import math
import pygame

from settings import(
    COLOR_BORDER, COLOR_TEXT_PRIMARY, COLOR_LEADERBOARD_TITLE,
    COLOR_OVERLAY, COLOR_PROMPT, COLOR_TEXT_SECONDARY, COLOR_VISION_CIRCLE,
    BORDER_THICKNESS, HUD_X_OFFSET, HUD_LINE_SPACING, HUD_Y_OFFSET,
    LEADERBOARD_Y_START, LEADERBOARD_Y_STEP)


class UIManager:
    def __init__(self, font):
        self.font = font

    def draw_world_border(self, screen, camera, world_width, world_height):
        top_left = camera.world_to_screen(0, 0)
        bottom_right = camera.world_to_screen(world_width, world_height)

        world_border = pygame.Rect(
            top_left[0],
            top_left[1],
            bottom_right[0] - top_left[0],
            bottom_right[1] - top_left[1],
        )

        pygame.draw.rect(screen, COLOR_BORDER, world_border, BORDER_THICKNESS)

    def draw_generation_counter(self, screen, generation_num, generation_time):
        gen_text = self.font.render(
            f"Generation: {generation_num}", True, COLOR_TEXT_PRIMARY
        )

        time_text = self.font.render(
            f"Time: {generation_time:.1f}s", True, COLOR_TEXT_SECONDARY
        )

        screen.blit(gen_text, (screen.get_width() // 2 - gen_text.get_width() // 2, 20))

        screen.blit(
            time_text, (screen.get_width() // 2 - time_text.get_width() // 2, 45)
        )

    def draw_leaderboard(self, screen, top_organisms, generation_num):
        overlay = pygame.Surface(
            (screen.get_width(), screen.get_height()), pygame.SRCALPHA
        )
        overlay.fill(COLOR_OVERLAY)
        screen.blit(overlay, (0, 0))

        # Title
        title_text = self.font.render(
            f"--- Generation {generation_num} Leaderboard ---", True, COLOR_LEADERBOARD_TITLE
        )
        screen.blit(
            title_text, (screen.get_width() // 2 - title_text.get_width() // 2, 100)
        )

        y = LEADERBOARD_Y_START
        for i, org in enumerate(top_organisms[:5], 1):
            text = self.font.render(
                f"{i}. Fitness: {org.fitness:.1f} | Food Eaten: {org.food_eaten} | Age: {org.age:.1f}",
                True,
                COLOR_TEXT_PRIMARY,
            )
            screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2, y))
            y += LEADERBOARD_Y_STEP

        prompt_text = self.font.render(
            "Press [ENTER] to start next generation", True, COLOR_PROMPT
        )
        screen.blit(
            prompt_text,
            (screen.get_width() // 2 - prompt_text.get_width() // 2, y + 60),
        )

    def draw_selection_and_hud(self, screen, camera, selected_organism, foods):
        if selected_organism is None:
            return

        screen_x, screen_y = camera.world_to_screen(
            selected_organism.x, selected_organism.y
        )

        # Vision radius circle
        pygame.draw.circle(
            screen,
            COLOR_VISION_CIRCLE,
            (screen_x, screen_y),
            int(selected_organism.vision * camera.zoom),
            1,
        )

        brain_inputs = selected_organism.get_brain_inputs(foods)
        brain_outputs = selected_organism.brain.predict(brain_inputs)

        stats = [
            f"Energy: {selected_organism.energy:.1f}",
            f"Speed: {selected_organism.speed:.2f}",
            f"Vision: {selected_organism.vision:.1f}",
            f"Brain Inputs:",
            f"  Energy:     {brain_inputs[0]:.2f}",
            f"  Food?:      {brain_inputs[1]:.1f}",
            f"  Distance:   {brain_inputs[2]:.2f}",
            f"  Angle (sin):{brain_inputs[3]:.2f}",
            f"  Angle (cos):{brain_inputs[4]:.2f}",
            f"  Time Food:  {brain_inputs[5]:.2f}",
            f"  Noise:      {brain_inputs[6]:.2f}",
            f"Brain Outputs:",
            f"  Turn:     {brain_outputs[0]:.2f}",
            f"  Movement: {brain_outputs[1]:.2f}",
        ]

        y = HUD_Y_OFFSET
        for stat in stats:
            text = self.font.render(stat, True, COLOR_TEXT_PRIMARY)
            screen.blit(text, (HUD_X_OFFSET, y))
            y += HUD_LINE_SPACING
