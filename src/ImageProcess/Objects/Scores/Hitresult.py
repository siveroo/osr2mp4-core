from ImageProcess import imageproc
from ImageProcess.Objects.FrameObject import FrameObject
from global_var import Settings, SkinPaths


class HitResult(FrameObject):
	def __init__(self, frames):
		super().__init__(frames)
		self.moveright = Settings.moveright
		self.movedown = Settings.movedown
		self.divide_by_255 = 1 / 255.0
		self.hitresults = []
		self.interval = Settings.timeframe / Settings.fps
		self.time = 600
		self.misscount = 0
		self.multiplieranimation = {0: 2, 50: 1, 100: 1, 300: 1}
		self.playfieldscale = Settings.playfieldscale

	def add_result(self, scores, x, y):
		"""
		:param scores: hitresult
		:param x: 0-512
		:param y: 0-384
		:return:
		"""
		x = int(x * self.playfieldscale) + self.moveright
		y = int(y * self.playfieldscale) + self.movedown

		if scores == 0:
			self.misscount += 1

		if scores == 300 and self.frames[300][0].size[0] == 1 and self.frames[300][0].size[1] == 1:
			return
		# [score, x, y, index, alpha, time, go down]
		self.hitresults.append([scores, x, y, 0, 40, 0, 3])

	def add_to_frame(self, background):
		i = len(self.hitresults)
		while i > 0:
			i -= 1

			score = self.hitresults[i][0]

			if self.hitresults[i][5] >= self.time * self.multiplieranimation[score]:
				del self.hitresults[i]
				if score == 0:
					self.misscount -= 1
				if self.misscount == 0:  # if there is no misscount then this is the last element so we can break
					break
				else:
					continue

			img = self.frames[score][int(self.hitresults[i][3])]

			x, y = self.hitresults[i][1], self.hitresults[i][2]
			imageproc.add(img, background, x, y, alpha=self.hitresults[i][4] / 100)

			if score == 0:
				self.hitresults[i][2] += int(self.hitresults[i][6] * self.playfieldscale)
				self.hitresults[i][6] = max(0.8, self.hitresults[i][6] - 0.2 * 60/Settings.fps)

			self.hitresults[i][3] = min(len(self.frames[score]) - 1, self.hitresults[i][3] + 1 * 60/Settings.fps)
			self.hitresults[i][5] += self.interval * SkinPaths.skin_ini.general["AnimationFramerate"]/Settings.fps

			if self.hitresults[i][5] >= self.time - self.interval * 10:
				self.hitresults[i][4] = max(0, self.hitresults[i][4] - (10/self.multiplieranimation[score]) * 60/Settings.fps)
			else:
				self.hitresults[i][4] = min(100, self.hitresults[i][4] + (20/self.multiplieranimation[score]) * 60/Settings.fps)

