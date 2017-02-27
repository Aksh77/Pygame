import pygame,sys
import DNA_Arcade as game
 
pygame.init()

myfont = pygame.font.SysFont('jokerman', 80)
 
class MenuItem(pygame.font.Font):
	def __init__(self, text, font=None, font_size=60,
				 font_color=(255, 255, 255), (pos_x, pos_y)=(0, 0)):
		pygame.font.Font.__init__(self, font, font_size)
		self.text = text
		self.font_size = font_size
		self.font_color = font_color
		self.label = self.render(self.text, 1, self.font_color)
		self.width = self.label.get_rect().width
		self.height = self.label.get_rect().height
		self.dimensions = (self.width, self.height)
		self.pos_x = pos_x
		self.pos_y = pos_y
		self.position = pos_x, pos_y
 
	def set_position(self, x, y):
		self.position = (x, y)
		self.pos_x = x
		self.pos_y = y
 
	def set_font_color(self, rgb_tuple):
		self.font_color = rgb_tuple
		self.label = self.render(self.text, 1, self.font_color)
 
	def is_mouse_selection(self, (posx, posy)):
		if (posx >= self.pos_x and posx <= self.pos_x + self.width) and \
			(posy >= self.pos_y and posy <= self.pos_y + self.height):
				return True
		return False
 
 
class GameMenu():
	def __init__(self, screen, items, funcs, bg_color=(0,0,0), font=None, font_size=60,
					font_color=(255, 255, 255)):
		self.screen = screen
		self.scr_width = self.screen.get_rect().width
		self.scr_height = self.screen.get_rect().height
		self.funcs=funcs
		self.bg_color = bg_color
		self.clock = pygame.time.Clock()
		self.items = []
		for index, item in enumerate(items):
			menu_item = MenuItem(item)
 
			# t_h: total height of text block
			t_h = len(items) * menu_item.height
			pos_x = (self.scr_width / 2) - (menu_item.width / 2)
			pos_y = (self.scr_height / 2) - (t_h / 2) + ((index * 2) + index * menu_item.height)
 
			menu_item.set_position(pos_x, pos_y)
			self.items.append(menu_item)
 
	def run(self):
		mainloop = True
		while mainloop:
			# Limit frame speed to 50 FPS
			self.clock.tick(50)
			
			mpos=pygame.mouse.get_pos()
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					mainloop = False
				if event.type==pygame.MOUSEBUTTONDOWN:
					for item in self.items:
						if item.is_mouse_selection(mpos):
							self.funcs[item.text]()
 
			# Redraw the background
			self.screen.fill(self.bg_color)
			label=myfont.render('DNA Arcade',1,(255,0,100))
			self.screen.blit(label,(60,50))
			#self.font_size
			for item in self.items:
				if item.is_mouse_selection(pygame.mouse.get_pos()):
					item.set_font_color((0, 100, 255))
				else:
					item.set_font_color((255, 255, 255))
				self.screen.blit(item.label, item.position)
 
			pygame.display.flip()

def menu():
	screen = pygame.display.set_mode((640, 480), 0, 32)
	menu_items = ('Start', 'Quit')
	s=pygame.font.get_fonts()
	print s
	pygame.display.set_caption('Game Menu')
	funcs = {'Start': game.main, 'Quit': sys.exit}
	gm = GameMenu(screen,funcs.keys(),funcs)
	gm.run()

if __name__ == "__main__":
	menu()
