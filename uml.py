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
| - __init__(col: int, row: int)                   |
| - __lt__(other: CellNode): bool                  |
| + drawGrid():   None                             |
| + drawVisit():  None                             |
| + drawTrail():  None                             |
| + drawSearch(): None                             |
| + drawBlock():  None                             |
| + drawActive(): None                             |
| + drawFocus():  None                             |
| + drawTarget(): None                             |
| + drawFinish(): None                             |
| + getRandomNeighbor(): CellNode                  |
| + hasWallBetween(other: CellNode):    bool       |
| + removeWallBetween(other: CellNode): None       | 
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
|   - moveSound(next: Optional[CellNode]):   None  | 
|   - interpolateMovement(next: CellNode):   None  |
|   - solve(start: CellNode, end: CellNode): None  |
|   - refresh(next: CellNode): None                |
|   - eventListener(): None                        |
|   - generate():  None                            |
|   + create():    None                            |
|   + render():    None                            |
|   - moveUp():    None                            |
|   - moveDown():  None                            |
|   - moveLeft():  None                            |
|   - moveRight(): None                            |
+--------------------------------------------------+