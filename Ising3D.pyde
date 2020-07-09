def setup():
    size(800, 800, P3D)
    background(255)
    global start_i
                
class Box:
    def __init__(self, x, y, z, r):
        self.x = x
        self.y = y
        self.z = z
        
        # Red value, which defines both initial spin and display color
        self.r = r
        
        if self.r == 0:
            self.spin = -1
            self.b = 255
        else:
            self.spin = 1
            self.b = 0
        
    def draw_box(self):
        translate(self.x, self.y, self.z)
        noStroke()
        fill(self.r, 0, self.b, 40)
        box(res)
        
        translate(-self.x, -self.y, -self.z)
        
    def flip_spin(self):
        self.spin *= -1
        if self.r == 0:
            self.r = 255
            self.b = 0
        else:
            self.r = 0
            self.b = 255
        
        
def energy(box_list, i, j, k):
    """Returns "energy" of spin alignment/antialignment arrangement"""
    curr = box_list[i][j][k].spin
    
    e = curr * box_list[i+1][j][k].spin
    e += curr * box_list[i-1][j][k].spin
    e += curr * box_list[i][j+1][k].spin
    e += curr * box_list[i][j-1][k].spin
    e += curr * box_list[i][j][k+1].spin
    e += curr * box_list[i][j][k-1].spin
    
    return -e


span = 270
boxes = []
res = 18
n = span // res

T = 100

for x in range(-span//2, span//2, res):
    b_sheet = []
    for y in range(-span//2, span//2, res):
        bs = []
        for z in range(-span//2, span//2, res):
            if random(1) < 0.5:
                bs.append(Box(x, y, z, 255))
            else:
                bs.append(Box(x, y, z, 0))
        b_sheet.append(bs)
    boxes.append(b_sheet)

start_i = 2

# If true, the system will rotate as the mouse is moved over the screen
rotate_bool = False

di = 1

def draw():
    global boxes, res, n, span, start_i, T, di
    # Decreasing system "temperature" with every run, encouraging energy minimization
    T *= .99
    clear()
    background(255)

    translate(width/2, height/2)
    if rotate_bool:
        rotateX(-(mouseY)/200. + PI)
        rotateY((mouseX+width/4)/200. - PI/2)
    else:
        rotateX(-5*PI/4 + PI/10)
        rotateY(PI/4)
    
    # if not rotate_bool:
    #     start_i = int(map(mouseX, 0, width, 1, n-1))
    
    for run in range(500):
        i = int(round(random(1,n-2)))
        j = int(round(random(1,n-2)))
        k = int(round(random(1,n-2)))
        
        e1 = energy(boxes, i, j, k)
        
        boxes[i][j][k].flip_spin()
        
        e2 = energy(boxes, i, j, k)
        
        if exp(-(e2-e1) / T) < random(1):
            boxes[i][j][k].flip_spin()
        
        # if e1 < e2:
        #     boxes[i][j][k].flip_spin()
    
    for i in range(1,n-1):
        for j in range(1,n-1):
            for k in range(int(start_i),n-1):
                b = boxes[i][j][k]
                b.draw_box()
                
    if T < 10:
        start_i += di/3.
    
    if int(round(start_i)) == n-2 or int(round(start_i)) == 1:
        di *= -1
                
def mouseClicked():
    global start_i
    if mouseX > width/2 and start_i > 1:
        start_i -= 1
    elif mouseX < width/2 and start_i < n-2:
        start_i += 1
    
    
        
        
