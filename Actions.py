from operator import truediv


class ModAction():
    trigger = -1
    def __init__(self, TargetCore, object, text):
        self.Core = TargetCore
        self.targettype = object
        self.text = text

    def triggercheck(self):
        if self.trigger > 0:
            self.doaction(self)
            return 1
        else:
            return -1

    def doaction(self,me):
        return

    def checkObject(self, object):
        if object.__class__ == self.targettype.__class__:
            return True
        return False

    def setTrigger(self, object):
        self.trigger = object


class ActionContainer():
    action = False
    def triggercheck(self):
        if self.action.triggercheck() > 0:
            self.action = False

    def hasAction(self):
        if self.action == False:
            return False
        return True

    def setTrigger(self, trigger):
        if self.action.checkObject(trigger):
            self.action.setTrigger(trigger)
            self.action.doaction()
            self.action = False
            return True
        return False

