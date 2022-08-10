class Queue :
 def __init__ (OO0OOO000O00OO0OO ): OO0OOO000O00OO0OO ._fuscat12 =[] ;
 def is_empty (OOOO00000000O0O00 ): return (OOOO00000000O0O00 ._fuscat12 == [] and True)
 def enqueue (O000000000OOOO0O0 ,OOOO000O000OO0O00 ): raise NotImplementedError
 def dequeue (O00O0OOOO0OOO0OOO ): raise NotImplementedError

class AddToEndQueue(Queue):
 def enqueue (O000000000OOOO0O0 ,OOOO000O000OO0O00 ):O000000000OOOO0O0 ._fuscat12 .append (OOOO000O000OO0O00)
 def dequeue (O00O0OOOO0OOO0OOO ):return O00O0OOOO0OOO0OOO ._fuscat12 .pop (0)

class AddToStartQueue (Queue):
 def enqueue (O000000000OOOO0O0 ,OOOO000O000OO0O00 ):O000000000OOOO0O0 ._fuscat12 .insert (0, OOOO000O000OO0O00)
 def dequeue (O00O0OOOO0OOO0OOO ):return O00O0OOOO0OOO0OOO ._fuscat12 .pop ()