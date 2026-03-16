import cv2
import pygame
import sys
import time
from tkinter import filedialog, Tk

class AspectPlayer:
    def __init__(self):
        pygame.init()
        
        root = Tk()
        root.withdraw()
        self.video_path = filedialog.askopenfilename(filetypes=[("Video", "*.mp4 *.avi")])
        if not self.video_path: sys.exit()

        self.cap = cv2.VideoCapture(self.video_path)
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.native_w = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.native_h = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        # Window Dimensions
        self.win_w, self.win_h = 1000, 600
        self.screen = pygame.display.set_mode((self.win_w, self.win_h), pygame.RESIZABLE | pygame.SCALED)
        pygame.display.set_caption("Python Aspect Ratio Player")

        # States
        self.playing = True
        self.fullscreen = False
        self.show_controls = True
        self.last_mouse_move = time.time()
        self.aspect_mode = 0  # 0: Fit, 1: Stretch, 2: Original
        self.modes_text = ["FIT", "STRETCH", "1:1"]
        
        # Control positions
        self.btn_y = self.win_h - 50
        self.centers = {
            "back": 350, "play": 420, "stop": 490, "fwd": 560,
            "aspect": 680, "full": 750
        }
        
        self.run()

    def get_video_surface(self, frame):
        """Processes frame based on aspect ratio mode."""
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        if self.aspect_mode == 0: # FIT (Letterbox)
            # Calculate scaling to fit window while keeping ratio
            video_ratio = self.native_w / self.native_h
            win_ratio = self.win_w / self.win_h
            
            if video_ratio > win_ratio:
                new_w = self.win_w
                new_h = int(new_w / video_ratio)
            else:
                new_h = self.win_h
                new_w = int(new_h * video_ratio)
                
            frame = cv2.resize(frame, (new_w, new_h))
            surf = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
            
            # Create a black background and center the video
            final_surf = pygame.Surface((self.win_w, self.win_h))
            final_surf.fill((0, 0, 0))
            final_surf.blit(surf, ((self.win_w - new_w)//2, (self.win_h - new_h)//2))
            return final_surf

        elif self.aspect_mode == 1: # STRETCH
            frame = cv2.resize(frame, (self.win_w, self.win_h))
            return pygame.surfarray.make_surface(frame.swapaxes(0, 1))

        else: # ORIGINAL (1:1)
            surf = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
            final_surf = pygame.Surface((self.win_w, self.win_h))
            final_surf.fill((0, 0, 0))
            final_surf.blit(surf, ((self.win_w - self.native_w)//2, (self.win_h - self.native_h)//2))
            return final_surf

    def draw_ui(self, current_frame):
        overlay = pygame.Surface((self.win_w, 110), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180)) 
        self.screen.blit(overlay, (0, self.win_h - 110))

        # Seek Bar
        bar_x, bar_y, bar_w, bar_h = 50, self.win_h - 95, 900, 6
        pygame.draw.rect(self.screen, (80, 80, 80), (bar_x, bar_y, bar_w, bar_h))
        prog = current_frame / self.total_frames if self.total_frames > 0 else 0
        pygame.draw.rect(self.screen, (0, 150, 255), (bar_x, bar_y, bar_w * prog, bar_h))
        
        # Draw Mode Text above button
        font = pygame.font.SysFont("Arial", 12, bold=True)
        txt = font.render(self.modes_text[self.aspect_mode], True, (255, 255, 255))
        self.screen.blit(txt, (self.centers["aspect"] - 20, self.btn_y - 45))

        for name, x in self.centers.items():
            self.draw_icon(name, x)

    def draw_icon(self, name, cx):
        cy = self.btn_y
        col = (255, 255, 255)
        if name == "aspect": # Aspect Ratio Icon (overlapping rectangles)
            pygame.draw.rect(self.screen, col, (cx-12, cy-8, 24, 16), 2)
            pygame.draw.rect(self.screen, (0, 150, 255), (cx-6, cy-4, 12, 8), 1)
        elif name == "play":
            pygame.draw.circle(self.screen, (60, 60, 60), (cx, cy), 25)
            if not self.playing: pygame.draw.polygon(self.screen, col, [(cx-8, cy-10), (cx-8, cy+10), (cx+12, cy)])
            else: 
                pygame.draw.rect(self.screen, col, (cx-8, cy-10, 6, 20))
                pygame.draw.rect(self.screen, col, (cx+2, cy-10, 6, 20))
        # ... (Other icons: back, stop, fwd, full - similar to previous code)
        elif name == "stop": pygame.draw.rect(self.screen, (200, 50, 50), (cx-10, cy-10, 20, 20))
        elif name == "back": pygame.draw.polygon(self.screen, col, [(cx, cy-8), (cx, cy+8), (cx-12, cy)])
        elif name == "fwd": pygame.draw.polygon(self.screen, col, [(cx, cy-8), (cx, cy+8), (cx+12, cy)])
        elif name == "full": pygame.draw.rect(self.screen, col, (cx-10, cy-10, 20, 20), 2)

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: return False
            if event.type in [pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN]:
                self.last_mouse_move = time.time()
                self.show_controls = True

            if event.type == pygame.MOUSEBUTTONDOWN and self.show_controls:
                mx, my = event.pos
                for name, x in self.centers.items():
                    if ((mx - x)**2 + (my - self.btn_y)**2)**0.5 < 30:
                        if name == "aspect": self.aspect_mode = (self.aspect_mode + 1) % 3
                        elif name == "play": self.playing = not self.playing
                        elif name == "full": self.toggle_fullscreen()
                        elif name == "stop": self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0); self.playing = False
                        elif name == "back": self.seek(-5)
                        elif name == "fwd": self.seek(5)
        return True

    def seek(self, secs):
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, max(0, self.cap.get(cv2.CAP_PROP_POS_FRAMES) + (secs * self.fps)))

    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        self.screen = pygame.display.set_mode((self.win_w, self.win_h), (pygame.FULLSCREEN if self.fullscreen else pygame.RESIZABLE) | pygame.SCALED)

    def run(self):
        while True:
            if not self.handle_input(): break
            if time.time() - self.last_mouse_move > 3: self.show_controls = False

            if self.playing:
                ret, frame = self.cap.read()
                if ret: self.current_frame_data = self.get_video_surface(frame)
                else: self.playing = False
            
            if self.current_frame_data: self.screen.blit(self.current_frame_data, (0, 0))
            if self.show_controls: self.draw_ui(int(self.cap.get(cv2.CAP_PROP_POS_FRAMES)))
            pygame.display.flip()
            pygame.time.Clock().tick(self.fps)
        self.cap.release(); pygame.quit()

if __name__ == "__main__":
    AspectPlayer()