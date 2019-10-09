from lib.game import Widget

class W_Bush(Widget):
    def activate(self, activator):
        if activator.direction == 'up':
            activator.yMomentum += 10
        elif activator.direction == 'left':
            activator.xMomentum += 10
        elif activator.direction == 'right':
            activator.xMomentum -= 10
        else:
            activator.yMomentum -= 10
        print('Punted ' + str(self))

class W_Jack(Widget):
    def activate(self, activator):
        # Face activator
        self.faceWidget(self, activator)
