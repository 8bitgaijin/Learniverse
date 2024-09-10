import arcade
import arcade.gui

# Set up constants for screen size and title
SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 1080
SCREEN_TITLE = "Learniverse"


# Base class for all game states
class GameState:
    def update(self):
        raise NotImplementedError("Must override update method")

    def render(self):
        raise NotImplementedError("Must override render method")

    def on_key_press(self, key, modifiers):
        pass

    def on_close(self):
        pass


# Intro state: first screen showing company name and waiting for key press or mouse click
class IntroState(GameState):
    def __init__(self, state_manager):
        self.state_manager = state_manager  # Reference to the state manager

    def update(self):
        # No automatic transition logic here
        pass

    def render(self):
        # Render intro text
        arcade.draw_text("Developed by:", SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.75,
                         arcade.color.RADICAL_RED, font_size=49, anchor_x="center")
        
        arcade.draw_text("Alvadore Retro Technology", SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.5,
                         arcade.color.RADICAL_RED, font_size=48, anchor_x="center")

    def on_key_press(self, key, modifiers):
        # Transition to the main menu when any key is pressed
        self.state_manager.set_state(MenuState(self.state_manager))

    def on_mouse_press(self, x, y, button, modifiers):
        # Transition to the main menu when the mouse is clicked
        self.state_manager.set_state(MenuState(self.state_manager))


# MenuState: main menu with buttons using the UI system
class MenuState(GameState):
    def __init__(self, state_manager):
        self.state_manager = state_manager  # Reference to the state manager
        self.manager = arcade.gui.UIManager()  # Manages the GUI components
        self.manager.enable()  # Enable the UI manager

        # Create a vertical box layout to organize buttons
        self.v_box = arcade.gui.UIBoxLayout()

        # Create the Start button
        start_button = arcade.gui.UIFlatButton(text="Start Game", width=200)
        self.v_box.add(start_button.with_space_around(bottom=20))

        # Create the Settings button
        settings_button = arcade.gui.UIFlatButton(text="Settings", width=200)
        self.v_box.add(settings_button.with_space_around(bottom=20))

        # Create the Quit button
        quit_button = arcade.gui.UIFlatButton(text="Quit", width=200)
        self.v_box.add(quit_button)

        # Connect button actions (Start button transitions to the game)
        start_button.on_click = self.on_click_start

        # Handle Settings button click with an inline function
        @settings_button.event("on_click")
        def on_click_settings(event):
            print("Settings selected")

        # Quit button closes the window
        @quit_button.event("on_click")
        def on_click_quit(event):
            arcade.get_window().close()

        # Center the buttons on the screen
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box)
        )

    def on_click_start(self, event):
        # Transition to the main game state
        self.state_manager.set_state(MainGameState())

    def update(self):
        pass

    def render(self):
        # Draw the menu buttons on the screen
        self.manager.draw()

    def on_close(self):
        """Handle cleanup for the UIManager when leaving the menu state"""
        self.manager.disable()


# MainGameState: the actual game state where the gameplay happens
class MainGameState(GameState):
    def __init__(self):
        # Initialize player position and movement speed
        self.player_x = SCREEN_WIDTH / 2
        self.player_y = SCREEN_HEIGHT / 2
        self.player_speed = 5  # Speed of player movement
        self.score = 0  # Track the player's score

    def update(self):
        # Handle movement logic for the player
        self.player_x += self.player_speed

        # Wrap the player around if they go off the screen
        if self.player_x > SCREEN_WIDTH:
            self.player_x = 0
            self.score += 1  # Increase score when wrapping

    def render(self):
        # Render the score and player (a circle)
        arcade.draw_text(f"Score: {self.score}", 10, SCREEN_HEIGHT - 40,
                         arcade.color.WHITE, font_size=20)
        arcade.draw_circle_filled(self.player_x, self.player_y, 20, arcade.color.BLUE)


# MainWindow: the main window that ties everything together
class MainWindow(arcade.Window):
    def __init__(self, game_config, state_manager):
        super().__init__(game_config.width, game_config.height, game_config.title)
        self.state_manager = state_manager  # Manages which state is active
        arcade.set_background_color(arcade.color.BLACK)  # Set the background color

    def on_draw(self):
        # Render the current state
        arcade.start_render()
        self.state_manager.render()

    def update(self, delta_time):
        # Update the current state each frame
        self.state_manager.update()

    def on_key_press(self, key, modifiers):
        # Handle key press events
        self.state_manager.on_key_press(key, modifiers)

    def on_mouse_press(self, x, y, button, modifiers):
        # Handle mouse press events
        self.state_manager.on_mouse_press(x, y, button, modifiers)

    def on_close(self):
        # Ensure cleanup when the window is closed
        self.state_manager.on_close()
        super().on_close()


# StateManager: handles transitions between different game states.
class StateManager:
    def __init__(self):
        self.current_state = IntroState(self)  # Start with the intro state

    def set_state(self, new_state: GameState):
        # Call on_close to properly clean up the current state before switching
        self.current_state.on_close()
        # Switch to the new game state
        self.current_state = new_state

    def update(self):
        # Update the current state (called each frame)
        self.current_state.update()

    def render(self):
        # Render the current state (called each frame)
        self.current_state.render()

    def on_key_press(self, key, modifiers):
        # Pass key press events to the current state
        self.current_state.on_key_press(key, modifiers)

    def on_mouse_press(self, x, y, button, modifiers):
        # Pass mouse press events to the current state
        if hasattr(self.current_state, "on_mouse_press"):
            self.current_state.on_mouse_press(x, y, button, modifiers)

    def on_close(self):
        # Handle any cleanup needed when exiting the state
        self.current_state.on_close()


# GameConfig: stores window properties like size and title.
class GameConfig:
    def __init__(self, width, height, title):
        self.width = width
        self.height = height
        self.title = title


# GameManager: responsible for running the game.
class GameManager:
    def __init__(self):
        # Create window and state manager
        self.game_config = GameConfig(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.state_manager = StateManager()

    def run(self):
        # Start game loop with a window and a state manager.
        game = MainWindow(self.game_config, self.state_manager)
        arcade.run()


# Run the game
if __name__ == "__main__":
    # Start the game manager
    game_manager = GameManager()
    game_manager.run()
