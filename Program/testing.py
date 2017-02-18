from data.DAO.SpellDAO import SpellDAO
from structure.spells.Spell import Spell



s = Spell(None,'cs','Mrazící fůze','Velká ohnivá koule zloby', 'a', 'b', 'c','d',5,'f')
SpellDAO().create_spell(s)