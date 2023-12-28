+--------------------------------------------------+
|                      CellNode                    |
+--------------------------------------------------+
| + row:         int                               |
| + col:         int                               |
| + x:           int                               |
| + y:           int                               |
| + w:           int                               |
| + block:       pygame.draw.Rect                  |
| + visited:     bool                              |
| + walls:       bool[4]                           |
| + neighbors:   CellNode[4]                       |
| + distance:    float                             |
| + predecessor: CellNode                          |
+--------------------------------------------------+
| - __init__(col: int, row: int)                   |   Tc: O(1) | Sc: O(1)
| - __lt__(other: CellNode): bool                  |   Tc: O(1) | Sc: O(1)
| + drawGrid():   None                             |   Tc: O(1) | Sc: O(1)
| + drawVisit():  None                             |   Tc: O(1) | Sc: O(1)
| + drawTrail():  None                             |   Tc: O(1) | Sc: O(1)
| + drawSearch(): None                             |   Tc: O(1) | Sc: O(1)
| + drawBlock():  None                             |   Tc: O(1) | Sc: O(1)
| + drawActive(): None                             |   Tc: O(1) | Sc: O(1)
| + drawFocus():  None                             |   Tc: O(1) | Sc: O(1)
| + drawTarget(): None                             |   Tc: O(1) | Sc: O(1)
| + drawFinish(): None                             |   Tc: O(1) | Sc: O(1)
| + getRandomNeighbor(): CellNode                  |   Tc: O(1) | Sc: O(1)
| + hasWallBetween(other: CellNode):    bool       |   Tc: O(1) | Sc: O(1)
| + removeWallBetween(other: CellNode): None       |   Tc: O(1) | Sc: O(1)
+--------------------------------------------------+



+--------------------------------------------------+
|                     Maze.py                      |
+--------------------------------------------------+
|     # ======= window config =======              |
|   + xOffset: int                                 |
|   + yOffset: int                                 |
|   + area:    int                                 |
|   + w:       int # cell width                    |
|   + screen:  pygame.display                      |
|     # ======= sound url =======                  |
|   + sound_move:   pygame.mixer.Sound             |
|   + sound_target: pygame.mixer.Sound             |
|   + sound_wall:   pygame.mixer.Sound             |
|   + sound_clear:  pygame.mixer.Sound             |
|   + sound_trail:  pygame.mixer.Sound             |
|   + sound_found:  pygame.mixer.Sound             |
|   + sound_level:  pygame.mixer.Sound             |
|     # ======= level variables =======            |
|   - alreadyFinish: CellNode[]                    |
|   - searched:      CellNode[]                    |
|   - target:        CellNode[]                    |
|   - finish:        CellNode[]                    |
|   - stack:         CellNode[]                    |
|   - grid :         CellNode[]                    |
|   - current: CellNode                            |
|   - # ======= level limits =======               |
|   - isAllowControl: bool                         |
|   + targetLimit:    int                          |
|   + level:          int                          |
+--------------------------------------------------+
|   - solve(start: CellNode, end: CellNode): None  |   Tc: O(V + E + P log P) | Sc: O(V)
|   - eventListener(): None                        |   Tc: O(N + M) | Sc: O(1)
|   + render():    None                            |   Tc: O(V + E) | Sc: O(1)
|   - generate():  None                            |   Tc: O(V + E) | Sc: O(V)
|   + create():    None                            |   Tc: O(V) | Sc: O(1)
|   - moveUp():    None                            |   Tc: O(1) | Sc: O(1)
|   - moveDown():  None                            |   Tc: O(1) | Sc: O(1)
|   - moveLeft():  None                            |   Tc: O(1) | Sc: O(1)
|   - moveRight(): None                            |   Tc: O(1) | Sc: O(1)
|   - refresh(next: CellNode): None                |   Tc: O(1) | Sc: O(1)
|   - moveSound(next: Optional[CellNode]):   None  |   Tc: O(1) | Sc: O(1)
|   - interpolateMovement(next: CellNode):   None  |   Tc: O(1) | Sc: O(1)
+--------------------------------------------------+