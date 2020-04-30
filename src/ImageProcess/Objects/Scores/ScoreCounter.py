from ImageProcess.Objects.FrameObject import FrameObject


class ScoreCounter(FrameObject):
	def __init__(self, frames, diff, gap, settings):
		super().__init__(frames)
		self.freeze = 0
		self.showscore = 0
		self.score = 0
		self.diff = diff
		self.width = settings.width
		self.height = settings.height
		self.gap = int(gap * settings.scale * 0.75)

	def set_score(self, freeze, score, showscore):
		"""
		:param freeze:
		:param score:
		:param showscore:
		:return:
		"""
		self.freeze = freeze
		self.score = score
		self.showscore = showscore

	def update_score(self, score):
		#self.score += int(hitvalue + (hitvalue * ((combo * self.diff_multiplier * mod) / 25)))
		self.score = score

	def bonus_score(self, score):
		self.score += score
		self.showscore += score

	def draw_score(self, score_string, background):
		x = self.width - (-self.gap + self.frames[0].size[0]) * len(score_string)
		y = self.frames[0].size[1] // 2
		for digit in score_string:
			self.frame_index = int(digit)
			super().add_to_frame(background, x, y)
			x += -self.gap + self.frames[0].size[0]

	def add_to_frame(self, background, cur_time):
		score_string = str(int(self.showscore))
		score_string = "0" * (8 - len(score_string)) + score_string
		self.draw_score(score_string, background)

		if cur_time >= self.freeze:
			add_up = max(7.27, (self.score - self.showscore)/12.72)
			if self.showscore + add_up > self.score:
				self.showscore = min(self.score, max(self.score - 1, self.showscore + 0.05))
			else:
				self.showscore += add_up
