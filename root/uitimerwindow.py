import ui
import app
import net
import localeInfo
import chat

DESCRIPTION = {
	0 : [ "d:/ymir work/ui/game/dungeon_list/incoming.png", "Sertifika Etkinliði", "Her Gün", "|cff00FF7F23:00", "|cff00ccff00:00", 52701, None, None, None, None, None, None  ], #img, title, level, group request, cooldown, item, dungeon desc
	1 : [ "d:/ymir work/ui/game/dungeon_list/incoming.png", "Ramazan Etkinliði", "Her Gün", "|cff00FF7F01:00", "|cff00ccff05:00", 30315, None, None, None, None, None, None  ],
	2 : [ "d:/ymir work/ui/game/dungeon_list/incoming.png", "Ay Iþýðý Etkinliði", "Pazartesi", "|cff00FF7F20:00", "|cff00ccff21:00", 50011, None, None, None, None, None, None  ],
	3 : [ "d:/ymir work/ui/game/dungeon_list/incoming.png", "Derece Puan Etkinliði", "Salý", "|cff00FF7F20:00", "|cff00ccff21:00", 61424, None, None, None, None, None, None  ],
	4 : [ "d:/ymir work/ui/game/dungeon_list/incoming.png", "Evcil Hayvan Etkinliði", "Salý", "|cff00FF7F18:00", "|cff00ccff19:00", 38055, None, None, None, None, None, None  ],
	5 : [ "d:/ymir work/ui/game/dungeon_list/incoming.png", "Oyma Taþý Etkinliði", "Çarþamba", "|cff00FF7F19:00", "|cff00ccff20:00", 30178, None, None, None, None, None, None  ],
	6 : [ "d:/ymir work/ui/game/dungeon_list/incoming.png", "Okey Kart Etkinliði", "Çarþamba Ve Perþembe", "|cff00FF7F21:00", "|cff00ccff22:00", 79506, None, None, None, None, None, None  ],
	7 : [ "d:/ymir work/ui/game/dungeon_list/incoming.png", "Altýgen Paketi Etkinliði", "Perþembe", "|cff00FF7F19:00", "|cff00ccff20:00", 50037, None, None, None, None, None, None  ],
	8 : [ "d:/ymir work/ui/game/dungeon_list/incoming.png", "Futbol Topu Etkinliði", "Cuma", "|cff00FF7F21:00", "|cff00ccff22:00", 50096, None, None, None, None, None, None  ],
	9 : [ "d:/ymir work/ui/game/dungeon_list/incoming.png", "Amorun Sandýðý Etkinliði", "Pazar", "|cff00FF7F21:00", "|cff00ccff22:00", 71147, None, None, None, None, None, None  ],
	10 : [ "d:/ymir work/ui/game/dungeon_list/incoming.png", "Cadýlar Bayramý Etkinliði", "Pazar", "|cff00FF7F22:00", "|cff00ccff23:00", 30321, None, None, None, None, None, None  ],	
}


def load_dungeon_desc():
	for x in xrange(11):
		f = open("%s/dungeon_desc/%d.txt" % (app.GetLocalePath(), x), "r")
		lines = [line.rstrip('\n') for line in f]
		global DESCRIPTION
		DESCRIPTION[x][11] = lines


class TimerBoard(ui.ImageBox):
	def __init__(self, parent, index):
		ui.ImageBox.__init__(self)
		self.SetParent(parent)
		self.index = index
		self.parent = parent
		self.__Build()

		load_dungeon_desc()

	def __del__(self):
		ui.ImageBox.__del__(self)

	def __Build(self):
			
		self.LoadImage("d:/ymir work/ui/game/dungeon_list/available.tga")
			
		self.Show()

		self.image = ui.MakeImageBox(self, ("d:/ymir work/ui/game/dungeon_list/%d.tga" % self.index), 3, 3)

		self.textLine = ui.MakeTextLine(self)
		self.textLine.SetPosition(46, -10)
		self.textLine.SetWindowHorizontalAlignLeft()
		self.textLine.SetHorizontalAlignLeft()
		self.textLine.SetText(DESCRIPTION[self.index][1])

		
		self.incoming = ui.MakeTextLine(self)
		self.incoming.SetPosition(150, 0)
		self.incoming.SetWindowHorizontalAlignLeft()
		self.incoming.SetHorizontalAlignLeft()
		self.incoming.SetText("In curand")

		self.endTime = 0

	def SetTimeLeft(self, time):
		self.endTime = app.GetGlobalTimeStamp() + time

	def UpdateTime(self, indexNum):
		if self.endTime - app.GetGlobalTimeStamp() > 0:
			m, s = divmod(self.endTime - app.GetGlobalTimeStamp(), 60)
			h, m = divmod(m, 60)

			self.incoming.SetText("")
			self.LoadImage("d:/ymir work/ui/game/dungeon_list/unavailable.tga")
		else:
			self.incoming.SetText("")
			self.LoadImage("d:/ymir work/ui/game/dungeon_list/available.tga")
			

	
	def OnMouseLeftButtonDown(self):
		self.parent.SetDescription(self.index)

	def Destroy(self):
		self.image = None
		self.textLine = None



class TimerWindow(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def LoadWindow(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "uiscript/timerwindow.py")
		except:
			import exception
			exception.Abort("TimerWindow.LoadWindow.LoadObject")

		try:
			self.titleBar = self.GetChild("TitleBar")
			self.itemSlot = self.GetChild("ItemSlot")
			self.listDesc = self.GetChild("ListDesc")
			self.scrollBar = self.GetChild("ScrollBar")
		except:
			import exception
			exception.Abort("TimerWindow.LoadWindow.BindObject")

		self.titleBar.SetCloseEvent(ui.__mem_func__(self.Close))

		self.itemSlot.SetOverInItemEvent(ui.__mem_func__(self.__OnOverInItem))
		self.itemSlot.SetOverOutItemEvent(ui.__mem_func__(self.__OnOverOutItem))

		self.listDesc.SetItemSize(225, 11)
		self.listDesc.SetScrollBar(self.scrollBar)


		self.timerBoards = []
		for x in xrange(11):
			board = TimerBoard(self, x)
			board.SetPosition(23, 50 * (x + 1) - 7)
			self.timerBoards.append(board)

		self.tooltip = None

		self.image = ui.ImageBox()
		self.image.SetParent(self)
		self.image.SetPosition(342, 36)

		self.textLine = ui.MakeTextLine(self)
		self.textLine.SetPosition(342 - 178, 36 - 85 - 142)

		self.textLine2 = ui.MakeTextLine(self)
		self.textLine2.SetPosition(28, -167)
		self.textLine2.SetWindowHorizontalAlignRight()
		self.textLine2.SetHorizontalAlignRight()

		self.textLine3 = ui.MakeTextLine(self)
		self.textLine3.SetPosition(28, -150)
		self.textLine3.SetWindowHorizontalAlignRight()
		self.textLine3.SetHorizontalAlignRight()

		self.textLine4 = ui.MakeTextLine(self)
		self.textLine4.SetPosition(28, -133)
		self.textLine4.SetWindowHorizontalAlignRight()
		self.textLine4.SetHorizontalAlignRight()

		self.index = 0
		self.SetDescription(0) #default

	def SetDescription(self, index):
		self.index = index
		self.image.LoadImage(DESCRIPTION[index][0])
		self.textLine.SetText(DESCRIPTION[index][1])
		self.itemSlot.SetItemSlot(0, DESCRIPTION[index][5])
		self.image.Show()
		self.textLine2.SetText(str(DESCRIPTION[index][2]))
		self.textLine3.SetText(str(DESCRIPTION[index][3]))
		self.textLine4.SetText(str(DESCRIPTION[index][4]))

		self.__ClearList()
		for line in DESCRIPTION[index][11]:
			textLine = ui.TextLine()
			textLine.SetParent(self.listDesc)
			textLine.Show()
			textLine.SetText(line)
			self.listDesc.AppendItem(textLine)

	def __ClearList(self):
		for item in self.listDesc.itemList:
			item = None

		self.listDesc.RemoveAllItems()

	def SetTimeLeft(self, index, time):
		self.timerBoards[index].SetTimeLeft(time);
	
	def SetToolTip(self, tooltip):
		self.tooltip = tooltip
		self.tooltip.Hide()

	def __OnOverInItem(self, slotIndex):
		self.tooltip.SetItemToolTip(DESCRIPTION[self.index][5])

	def __OnOverOutItem(self):
		self.tooltip.HideToolTip()

	def Open(self):
		self.Show()

	def Close(self):
		self.Hide()

	def OnUpdate(self):
		for x in xrange(11):
			self.timerBoards[x].UpdateTime(x)

	def OnScrollWheel(self, len):
		if len >= 0:
			self.scrollBar.OnUp()
		else:
			self.scrollBar.OnDown()
		return True
		
	def OnRunMouseWheel(self, nLen):
		if nLen > 0:
			self.scrollBar.OnUp()
		else:
			self.scrollBar.OnDown()

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def Destroy(self):
		self.ClearDictionary()
		self.image = None
		self.textLine = None
		self.textLine2 = None
		self.textLine3 = None
		self.textLine4 = None
		self.titleBar = None
		self.itemSlot = None
		self.listDesc = None
		self.scrollBar = None
		for t in self.timerBoards:
			t.Destroy()
			t = None
		del self.timerBoards[:]
