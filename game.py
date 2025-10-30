import pygame
import serial
import sys
import random
import math
import time
import numpy as np

# Initialize Pygame and mixer
pygame.init()
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)

# Game constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_SIZE = 20
ENEMY_SIZE = 15
PLAYER_SPEED = 8
ENEMY_SPEED = 2
ENEMY_COUNT = 5

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 100, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)

class SoundManager:
    def __init__(self):
        self.sounds = {}
        self.load_sounds()
        
    def load_sounds(self):
        """Generate all sound effects"""
        try:
            self.generate_sound('move', self.create_whoosh_sound)
            self.generate_sound('collision', self.create_explosion_sound)
            self.generate_sound('score', self.create_beep_sound)
            self.generate_sound('powerup', self.create_chime_sound)
            self.generate_sound('game_start', self.create_startup_sound)
            self.generate_sound('game_over', self.create_game_over_sound)
            self.generate_sound('enemy_spawn', self.create_spawn_sound)
            print("✅ All sounds generated successfully!")
        except Exception as e:
            print(f"❌ Sound generation failed: {e}")
    
    def generate_sound(self, name, sound_function):
        """Generate a sound using the provided function"""
        try:
            sound_array = sound_function()
            # Convert to proper format for pygame
            sound_array = np.asarray(sound_array, dtype=np.int16)
            sound_array = np.column_stack((sound_array, sound_array))  # Stereo
            sound = pygame.sndarray.make_sound(sound_array)
            self.sounds[name] = sound
        except Exception as e:
            print(f"❌ Failed to generate sound '{name}': {e}")
    
    def create_whoosh_sound(self):
        """Create whoosh sound for movement"""
        duration = 0.3
        sample_rate = 44100
        samples = int(duration * sample_rate)
        sound_data = []
        
        for i in range(samples):
            t = i / sample_rate
            freq = 400 - 200 * (t / duration)  # Descending frequency
            volume = 0.3 * (1 - t/duration)    # Fade out
            sample = int(32767 * volume * math.sin(2 * math.pi * freq * t))
            sound_data.append(sample)
        
        return sound_data
    
    def create_explosion_sound(self):
        """Create explosion sound for collisions"""
        duration = 0.5
        sample_rate = 44100
        samples = int(duration * sample_rate)
        sound_data = []
        
        for i in range(samples):
            t = i / sample_rate
            # Low frequency rumble with noise
            rumble = math.sin(2 * math.pi * 60 * t)
            noise = random.uniform(-0.5, 0.5)
            
            if t < 0.1:
                volume = t / 0.1  # Quick attack
            else:
                volume = max(0, 1 - (t - 0.1) / 0.4)  # Slow decay
                
            sample = int(32767 * volume * (rumble * 0.7 + noise * 0.3))
            sound_data.append(sample)
        
        return sound_data
    
    def create_beep_sound(self):
        """Create beep sound for scoring"""
        duration = 0.2
        sample_rate = 44100
        samples = int(duration * sample_rate)
        sound_data = []
        
        for i in range(samples):
            t = i / sample_rate
            freq = 800 + 400 * math.sin(t * 10)  # Wobbly frequency
            volume = 0.5 * (1 - t/duration)      # Fade out
            sample = int(32767 * volume * math.sin(2 * math.pi * freq * t))
            sound_data.append(sample)
        
        return sound_data
    
    def create_chime_sound(self):
        """Create magical chime sound"""
        duration = 0.4
        sample_rate = 44100
        samples = int(duration * sample_rate)
        sound_data = []
        
        for i in range(samples):
            t = i / sample_rate
            # Multiple harmonious frequencies
            wave1 = math.sin(2 * math.pi * 523.25 * t)  # C5
            wave2 = math.sin(2 * math.pi * 659.25 * t)  # E5
            wave3 = math.sin(2 * math.pi * 783.99 * t)  # G5
            volume = 0.4 * math.exp(-3 * t)  # Exponential decay
            sample = int(32767 * volume * (wave1 + wave2 + wave3) / 3)
            sound_data.append(sample)
        
        return sound_data
    
    def create_startup_sound(self):
        """Create game startup sound"""
        duration = 0.8
        sample_rate = 44100
        samples = int(duration * sample_rate)
        sound_data = []
        
        for i in range(samples):
            t = i / sample_rate
            freq = 200 + 600 * (t / duration)  # Rising frequency
            volume = 0.6 * (t / duration)      # Fade in
            sample = int(32767 * volume * math.sin(2 * math.pi * freq * t))
            sound_data.append(sample)
        
        return sound_data
    
    def create_game_over_sound(self):
        """Create sad game over sound"""
        duration = 1.0
        sample_rate = 44100
        samples = int(duration * sample_rate)
        sound_data = []
        
        for i in range(samples):
            t = i / sample_rate
            freq = 400 - 350 * (t / duration)  # Descending frequency
            volume = 0.7 * (1 - t/duration)    # Fade out
            sample = int(32767 * volume * math.sin(2 * math.pi * freq * t))
            sound_data.append(sample)
        
        return sound_data
    
    def create_spawn_sound(self):
        """Create enemy spawn sound"""
        duration = 0.3
        sample_rate = 44100
        samples = int(duration * sample_rate)
        sound_data = []
        
        for i in range(samples):
            t = i / sample_rate
            freq = 300 - 250 * (t / duration)  # Descending frequency
            volume = 0.4 * (1 - t/duration)    # Fade out
            sample = int(32767 * volume * math.sin(2 * math.pi * freq * t))
            sound_data.append(sample)
        
        return sound_data
    
    def play(self, sound_name, volume=1.0):
        """Play a sound effect"""
        if sound_name in self.sounds:
            try:
                sound = self.sounds[sound_name]
                sound.set_volume(volume)
                sound.play()
            except Exception as e:
                print(f"❌ Could not play sound '{sound_name}': {e}")
    
    def stop_all(self):
        """Stop all currently playing sounds"""
        pygame.mixer.stop()

class Player:
    def __init__(self, sound_manager):
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2
        self.size = PLAYER_SIZE
        self.sound_manager = sound_manager
        self.last_move_time = 0
        self.move_sound_delay = 0.2  # seconds between move sounds
        
    def move(self, dx, dy):
        # Check if actually moving
        is_moving = abs(dx) > 0.1 or abs(dy) > 0.1
        
        # Apply movement
        self.x += dx * PLAYER_SPEED
        self.y += dy * PLAYER_SPEED
        
        # Keep player on screen
        self.x = max(self.size, min(SCREEN_WIDTH - self.size, self.x))
        self.y = max(self.size, min(SCREEN_HEIGHT - self.size, self.y))
        
        # Play movement sound with delay to avoid spam
        current_time = time.time()
        if is_moving and current_time - self.last_move_time > self.move_sound_delay:
            self.sound_manager.play('move', volume=0.2)
            self.last_move_time = current_time
    
    def draw(self, screen):
        pygame.draw.circle(screen, BLUE, (int(self.x), int(self.y)), self.size)
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), self.size // 2)

class Enemy:
    def __init__(self, sound_manager):
        self.size = ENEMY_SIZE
        self.speed = ENEMY_SPEED
        self.sound_manager = sound_manager
        self.respawn()
        
    def respawn(self):
        side = random.choice(['top', 'right', 'bottom', 'left'])
        if side == 'top':
            self.x = random.randint(0, SCREEN_WIDTH)
            self.y = -self.size
        elif side == 'right':
            self.x = SCREEN_WIDTH + self.size
            self.y = random.randint(0, SCREEN_HEIGHT)
        elif side == 'bottom':
            self.x = random.randint(0, SCREEN_WIDTH)
            self.y = SCREEN_HEIGHT + self.size
        else:  # left
            self.x = -self.size
            self.y = random.randint(0, SCREEN_HEIGHT)
            
    def update(self, player_x, player_y):
        dx = player_x - self.x
        dy = player_y - self.y
        dist = max(1, math.sqrt(dx*dx + dy*dy))
        
        self.x += dx / dist * self.speed
        self.y += dy / dist * self.speed
        
        if (self.x < -100 or self.x > SCREEN_WIDTH + 100 or 
            self.y < -100 or self.y > SCREEN_HEIGHT + 100):
            self.respawn()
    
    def draw(self, screen):
        pygame.draw.circle(screen, RED, (int(self.x), int(self.y)), self.size)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("🎵 MPU6050 Tilt Game with SOUND!")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        # Initialize sound manager first
        self.sound_manager = SoundManager()
        
        # Create game objects with sound manager
        self.player = Player(self.sound_manager)
        self.enemies = [Enemy(self.sound_manager) for _ in range(ENEMY_COUNT)]
        
        self.score = 0
        self.game_over = False
        self.last_score_sound = 0
        
        # MPU6050 data
        self.current_pitch = 0
        self.current_roll = 0
        self.mpu_connected = False
        self.mpu_initialized = False
        self.waiting_for_sensor = True
        self.start_time = time.time()
        
        # Play startup sound after a short delay
        pygame.time.delay(500)
        self.sound_manager.play('game_start', volume=0.8)
        
        # Initialize serial connection
        self.initialize_mpu()
        
    def initialize_mpu(self):
        """Initialize MPU6050 connection and wait for first data"""
        try:
            print("🔄 Initializing MPU6050 connection...")
            self.ser = serial.Serial('COM6', 115200, timeout=0.1)
            self.ser.reset_input_buffer()
            print("✅ Serial port opened on COM6")
            
            # Wait for first valid data with timeout
            print("⏳ Waiting for MPU6050 data...")
            max_wait_time = 5  # seconds
            start_wait = time.time()
            
            while time.time() - start_wait < max_wait_time:
                if self.ser.in_waiting > 0:
                    raw_data = self.ser.read(self.ser.in_waiting).decode('utf-8', errors='ignore')
                    lines = raw_data.split('\n')
                    
                    for line in reversed(lines):
                        line = line.strip()
                        if line and ',' in line:
                            pitch, roll = self.parse_mpu_data(line)
                            if pitch is not None and roll is not None:
                                self.current_pitch = pitch
                                self.current_roll = roll
                                self.mpu_connected = True
                                self.mpu_initialized = True
                                self.waiting_for_sensor = False
                                print("🎉 MPU6050 initialized successfully!")
                                # Play success sound
                                self.sound_manager.play('powerup', volume=0.6)
                                return
                
                # Show progress
                elapsed = time.time() - start_wait
                print(f"⏰ Waiting... {elapsed:.1f}s/{max_wait_time}s")
                time.sleep(0.1)
            
            # If we get here, timeout occurred
            print("❌ Timeout: No MPU6050 data received")
            self.ser.close()
            self.ser = None
            self.waiting_for_sensor = False
            
        except Exception as e:
            print(f"❌ Failed to initialize MPU6050: {e}")
            self.ser = None
            self.mpu_connected = False
            self.waiting_for_sensor = False
        
    def parse_mpu_data(self, line):
        """Parse the pitch,roll data from Arduino"""
        try:
            line = line.strip()
            if not line:
                return None, None
                
            parts = line.split(',')
            if len(parts) != 2:
                return None, None
                
            pitch = float(parts[0])
            roll = float(parts[1])
            return pitch, roll
            
        except:
            return None, None
        
    def handle_mpu_input(self):
        """Handle MPU6050 tilt input"""
        if not self.ser or not self.mpu_initialized:
            return False
            
        try:
            if self.ser.in_waiting > 0:
                raw_data = self.ser.read(self.ser.in_waiting).decode('utf-8', errors='ignore')
                lines = raw_data.split('\n')
                
                for line in reversed(lines):
                    line = line.strip()
                    if line and ',' in line:
                        pitch, roll = self.parse_mpu_data(line)
                        if pitch is not None and roll is not None:
                            self.current_pitch = pitch
                            self.current_roll = roll
                            
                            # Convert to movement
                            dx = -roll / 25.0
                            dy = pitch / 25.0
                            
                            # Minimal deadzone
                            deadzone = 0.1
                            if abs(dx) < deadzone: dx = 0
                            if abs(dy) < deadzone: dy = 0
                            
                            # Move player
                            self.player.move(dx, dy)
                            return True
                            
        except Exception as e:
            print(f"MPU read error: {e}")
                
        return False
        
    def handle_keyboard_input(self):
        """Handle keyboard input as fallback"""
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx = -1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx = 1
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy = -1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy = 1
            
        if dx != 0 or dy != 0:
            self.player.move(dx, dy)
            return True
            
        return False
    
    def handle_input(self):
        if self.mpu_initialized and self.ser:
            self.handle_mpu_input()
        else:
            self.handle_keyboard_input()
    
    def update(self):
        if self.game_over or self.waiting_for_sensor:
            return
            
        self.score += 1
        
        # Play score sound every 100 points
        if self.score % 100 == 0:
            current_time = time.time()
            if current_time - self.last_score_sound > 1.0:  # Avoid sound spam
                self.sound_manager.play('score', volume=0.4)
                self.last_score_sound = current_time
        
        # Update enemies
        for enemy in self.enemies:
            enemy.update(self.player.x, self.player.y)
            
            # Check collision
            distance = math.sqrt(
                (self.player.x - enemy.x)**2 + 
                (self.player.y - enemy.y)**2
            )
            if distance < self.player.size + enemy.size:
                self.game_over = True
                # Play collision sound
                self.sound_manager.play('collision', volume=0.7)
                # Play game over sound after a short delay
                pygame.time.delay(500)
                self.sound_manager.play('game_over', volume=0.6)
    
    def draw_waiting_screen(self):
        """Draw screen while waiting for MPU6050 to initialize"""
        self.screen.fill(BLACK)
        
        # Animated loading text
        elapsed = time.time() - self.start_time
        dots = "." * (int(elapsed * 2) % 4)
        
        title = self.font.render("🎵 MPU6050 TILT GAME WITH SOUND!", True, WHITE)
        waiting_text = self.font.render(f"Initializing Sensor{dots}", True, YELLOW)
        info_text = self.small_font.render("Please wait while the MPU6050 calibrates...", True, WHITE)
        tip_text = self.small_font.render("Keep the sensor still during initialization", True, ORANGE)
        
        self.screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 200))
        self.screen.blit(waiting_text, (SCREEN_WIDTH//2 - waiting_text.get_width()//2, 250))
        self.screen.blit(info_text, (SCREEN_WIDTH//2 - info_text.get_width()//2, 300))
        self.screen.blit(tip_text, (SCREEN_WIDTH//2 - tip_text.get_width()//2, 330))
        
        # Draw progress bar
        progress_width = 400
        progress_height = 20
        progress_x = SCREEN_WIDTH//2 - progress_width//2
        progress_y = 380
        
        # Background
        pygame.draw.rect(self.screen, (50, 50, 50), 
                        (progress_x, progress_y, progress_width, progress_height))
        
        # Progress
        progress = min(1.0, elapsed / 5.0)  # 5 second max wait
        pygame.draw.rect(self.screen, GREEN, 
                        (progress_x, progress_y, int(progress_width * progress), progress_height))
        
        pygame.display.flip()
    
    def draw(self):
        if self.waiting_for_sensor:
            self.draw_waiting_screen()
            return
            
        self.screen.fill(BLACK)
        
        # Draw player and enemies
        self.player.draw(self.screen)
        for enemy in self.enemies:
            enemy.draw(self.screen)
        
        # Draw score
        score_text = self.font.render(f"Score: {self.score}", True, GREEN)
        self.screen.blit(score_text, (10, 10))
        
        # Draw MPU data
        mpu_text = self.font.render(f"Pitch: {self.current_pitch:5.1f}° Roll: {self.current_roll:5.1f}°", True, YELLOW)
        self.screen.blit(mpu_text, (10, 50))
        
        # Draw control method
        if self.mpu_initialized:
            control_text = self.font.render("Control: 🎮 MPU6050 - READY!", True, GREEN)
            status_text = self.font.render("🔊 SOUND ON - TILT TO MOVE", True, GREEN)
        else:
            control_text = self.font.render("Control: ⌨️ Keyboard (MPU failed)", True, RED)
            status_text = self.font.render("🔊 Using arrow keys to move", True, YELLOW)
            
        self.screen.blit(control_text, (10, 90))
        self.screen.blit(status_text, (SCREEN_WIDTH - 400, 10))
        
        # Draw game over
        if self.game_over:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(180)
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))
            
            game_over_text = self.font.render("💥 GAME OVER 💥", True, RED)
            restart_text = self.font.render("Press R to restart or ESC to quit", True, WHITE)
            final_score = self.font.render(f"Final Score: {self.score}", True, GREEN)
            
            self.screen.blit(game_over_text, (SCREEN_WIDTH//2 - 120, SCREEN_HEIGHT//2 - 60))
            self.screen.blit(final_score, (SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 - 20))
            self.screen.blit(restart_text, (SCREEN_WIDTH//2 - 180, SCREEN_HEIGHT//2 + 20))
        
        pygame.display.flip()
    
    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r and self.game_over:
                        # Restart game
                        self.sound_manager.play('game_start', volume=0.7)
                        self.player = Player(self.sound_manager)
                        self.enemies = [Enemy(self.sound_manager) for _ in range(ENEMY_COUNT)]
                        self.score = 0
                        self.game_over = False
                        self.current_pitch = 0
                        self.current_roll = 0
                    elif event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_SPACE and self.waiting_for_sensor:
                        # Skip waiting
                        self.waiting_for_sensor = False
                        self.sound_manager.play('powerup')
                        print("⏩ Skipped sensor initialization")
                    elif event.key == pygame.K_m:
                        # Mute/unmute sounds
                        if pygame.mixer.get_volume() > 0:
                            pygame.mixer.set_volume(0)
                            print("🔇 Sound muted")
                        else:
                            pygame.mixer.set_volume(1.0)
                            print("🔊 Sound unmuted")
            
            if not self.waiting_for_sensor:
                self.handle_input()
                self.update()
            
            self.draw()
            self.clock.tick(60)
        
        # Clean up
        self.sound_manager.stop_all()
        if self.ser:
            self.ser.close()
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    print("🎵 Starting MPU6050 Tilt Game with SOUND EFFECTS!")
    print("📋 Sound Features:")
    print("   - Movement whooshes")
    print("   - Collision explosions") 
    print("   - Score celebration beeps")
    print("   - Game start/end sounds")
    print("   - Enemy spawn sounds")
    print("   - Press M to mute/unmute")
    
    game = Game()
    game.run()