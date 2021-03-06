from hearthy.protocol import mtypes
from hearthy.tracker.world import World
from hearthy.tracker.entity import Entity, TAG_CUSTOM_NAME, TAG_POWER_NAME

class Processor:
    def __init__(self):
        self._world = World()

    def process(self, who, what):
        with self._world.transaction() as t:
            self._process(who, what, t)

    def _process(self, who, what, t):
        if isinstance(what, mtypes.StartGameState):
            eid, taglist = (what.GameEntity.Id,
                            [(t.Name, t.Value) for t in what.GameEntity.Tags])
            taglist.append((TAG_CUSTOM_NAME, 'TheGame'))
            t.add(Entity(eid, taglist))

            for player in what.Players:
                eid, taglist = (player.Entity.Id,
                                [(t.Name, t.Value) for t in player.Entity.Tags])
                # TODO: are we interested in the battlenet id?
                taglist.append((TAG_CUSTOM_NAME, 'Player{0}'.format(player.Id)))
                t.add(Entity(eid, taglist))
        elif isinstance(what, mtypes.PowerHistory):
            for power in what.List:
                self._process_power(power, t)

    def _process_power(self, power, t):
        if hasattr(power, 'FullEntity'):
            e = power.FullEntity
            taglist = [(e.Name, e.Value) for e in e.Tags]
            taglist.append((TAG_POWER_NAME, e.Name))
            t.add(Entity(e.Entity, taglist))
        if hasattr(power, 'ShowEntity'):
            e = power.ShowEntity
            mut = t.get_mutable(e.Entity)
            mut[TAG_POWER_NAME] = e.Name
            for tag in e.Tags:
                mut[tag.Name] = tag.Value
        if hasattr(power, 'HideEntity'):
            pass
        if hasattr(power, 'TagChange'):
            change = power.TagChange
            e = t.get_mutable(change.Entity)
            e[change.Tag] = change.Value
