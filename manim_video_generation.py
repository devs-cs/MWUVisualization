from manim import *
from manim.mobject.text.text_mobject import remove_invisible_chars
import numpy as np

def WHACK(i, x_hat, C, epsilon, lam):
    z = x_hat.copy() 
    for j in range(len(x_hat)):
        z[j] *= (1 + epsilon * C[i,j] / lam)
    return z

def disArr(x):
    return "[" + ", ".join(list(map(str,x))) + "]"

class MWUVisualization(Scene):
    def construct(self):
        # The code string for MWU python function (done with numpy)

        mwu_code_str = '''def MWU(C, m, n, epsilon = 0.1, lam = 2):
    T = np.ceil(np.log(n) / epsilon**2 * lam).astype(int)
    x_hat = np.ones(n)
    x = x_hat * (x_hat[0] / np.linalg.norm(x_hat, 1))
    y = np.zeros((T, m))
    for t in range(T):
        if np.all(C @ x >= 1 - epsilon):
            return x, None
        for i in range(m):
            if (C @ x)[i] < 1:
                for j in range(len(x_hat)):
                    x_hat[j] *= (1 + epsilon * C[i,j] / lam)
                break
        x = x_hat / np.linalg.norm(x_hat, 1)
        y[t, i] = 1
    y_avg = np.sum(y, axis=0) / T
    return None, y_avg'''
        
        # Initialize algo params
        epsilon = 0.1
        lam = 2.0
        C = np.array([[1.3, 1.5, 0.5], [1.4, 0.2, 0.5], [0.7, -.1, 2]])  # Example C matrix
        m, n = C.shape
        T = int(np.ceil(np.log(n) / epsilon**2 * lam))
        x_hat = np.ones(n)
        x = x_hat * (x_hat[0]/np.linalg.norm(x_hat, 1))
        y = np.zeros((T, m))
        code = self.build_code_block(mwu_code_str)

        # mwu_code = Code(code=mwu_code_str, language="Python", background = "window",line_spacing = 1)
        # mwu_code.code = remove_invisible_chars(mwu_code.code)
        # code = self.build_code_block(mwu_code_str)
        # code.arrange(DOWN, buff = 1)
        # code.to_edge(LEFT)

        # code_group.code = remove_invisible_chars(code_group.code)
        # self.play(FadeIn(code))
        
        t_text  = MathTex(r"T = ", np.round(T,2)).scale(0.7)
        x_hat_text = MathTex(r"\hat{x} = ", disArr(np.round(x_hat, 2))).scale(0.7)
        x_text = MathTex(r"x = ", disArr(np.round(x, 2))).scale(0.7)
        y_text = MathTex(f"y_{1} = ", disArr(np.round(y[0], 2))).scale(0.7)
        C_text = Matrix(C).scale(0.5)


        C_text.move_to([5,3,0])
        self.play(Create(C_text))   

        self.highlight(0,1)
        t_text.move_to([5,1.8,0])
        self.play(Create(t_text))   
        self.highlight(1,2)
        x_hat_text.move_to([5,1,0])
        self.play(Create(x_hat_text))   
        self.highlight(2,3)
        x_text.move_to([5,0.2,0])
        self.play(Create(x_text))   
        self.highlight(3,4)
        y_text.move_to([5,-0.6, 0])
        self.play(Create(y_text))  
        self.highlight(4,5)
        
        

        # variable_group = VGroup(x_hat_text, x_text, y_text, C_text)
        # variable_group.arrange(DOWN, aligned_edge=LEFT)
        # variable_group.to_corner(UR)
        # self.play(FadeIn(variable_group))

        # Caption at the bottom of the screen
        caption = Text("", font_size=30).to_edge(DOWN)
        self.add(caption)
       
        x_broke = False
        
        # Logic for the MWU algorithim with included highlighting
        prior_line = 4
        for t in range(T):
            self.remove(caption)
            self.highlight(prior_line,5)
            t_text_new = MathTex(r"t = ", t, " | " , r"T = ", np.round(T,2)).scale(0.7)
            t_text_new.move_to([5,1.8,0])
            self.play(Transform(t_text, t_text_new))
            self.remove(caption)
            caption = Text("Checking if all constraints are satisfied", font_size=30).to_edge(DOWN)
            self.add(caption)
            self.highlight(5,6)
 
            if np.all(np.matmul(C, x) >= 1 - epsilon):
                self.highlight(6,7)
                self.remove(caption)
                caption = Text("All constraints are satisfied", font_size=30).to_edge(DOWN)
                self.add(caption)
                prior_line = 7

                break  
            self.highlight(6,8)
            
            prior_line = 9
            for_break = False
            for i in range(m):
                self.highlight(8,9)
                if np.matmul(C, x)[i] < 1:
                    
                    self.remove(caption)
                    caption = Text(f"The constraint {i+1} is not satisfied: {disArr(np.round(C[i],2))} * {disArr(np.round(x,2))} = {np.round(np.matmul(C, x)[i],2)} < 1", font_size=25).to_edge(DOWN)
                    
                    self.add(caption)
                    self.highlight(prior_line,10)
                    
                    x_hat = WHACK(i, x_hat, C, epsilon, lam)  #WHACK
                    self.remove(caption)
                    caption = Text(f"Running WHACK on x_hat", font_size=30).to_edge(DOWN)
                    self.add(caption)
                    self.highlight(10,12)
                    
                    
                    
                    x = x_hat / np.linalg.norm(x_hat, 1)  # Update x
                    # self.remove(x_hat_text)
                    x_hat_text_new = MathTex(r"\hat{x} = ", disArr(np.round(x_hat, 2))).scale(0.7)
                    x_hat_text_new.move_to([5,1,0])
                    self.play(Transform(x_hat_text, x_hat_text_new ))
                    # variable_group.add(x_hat_text)
                    # self.play(Create(variable_group))
                    
                    self.highlight(12,13)
                    

                    self.remove(caption)
                    caption = Text("Updating vector x", font_size=30).to_edge(DOWN)
                    self.add(caption)

                    x_text_new = MathTex(r"x = ", disArr(np.round(x, 2))).scale(0.7)
                    x_text_new.move_to([5,0.2,0])
                    self.play(Transform(x_text, x_text_new))

                    self.highlight(13,14)

                    # variable_group.add(x_hat_text,x_text)
                    # self.play(Create(variable_group))
                   
                    self.remove(caption)
                    caption = Text("Updating vector y", font_size=30).to_edge(DOWN)
                    self.add(caption)

                    prior_line = 14

                    y[t, i] = 1  # Update y
                    y_text_new = MathTex(f"y_{t+1} = ", disArr(np.round(y[t], 2))).scale(0.7)
                    y_text_new.move_to([5,-0.6, 0])
                    self.play(Transform(y_text,y_text_new))
                      # Handle only one constraint
                    break

        # Calculate and display y_avg
        if (not x_broke):
            self.highlight(prior_line,13)
            self.remove(caption)
            caption.set_value("t = T, calculating average of y over iterations to return.")
            self.add(caption)
            y_avg = np.sum(y, axis=0) / T
            y_avg_text = MathTex(r"\bar{y} = ", disArr(np.round(y_avg, 2))).scale(0.7)
            y_avg_text.move_to([5, -2, 0])
            self.play(FadeIn(y_avg_text))
            self.wait(2)
            
        self.play(FadeOut(caption))

    def build_code_block(self, code_str):
        # build the code block
        code = Code(code=code_str, language='python', background="window", font_size = 15).to_corner(UL)
        code.code = remove_invisible_chars(code.code)
        self.add(code)
        # build sliding windows (SurroundingRectangle)
        self.sliding_wins = VGroup()
        height = code.code[0].height
        for line in code.code:
            self.sliding_wins.add(SurroundingRectangle(line).set_fill(YELLOW).set_opacity(0))

        self.add(self.sliding_wins)
        return code
        
        # Function to highlight lines in the code
    def highlight(self, prev_line, line):
        # self.play(self.sliding_wins[prev_line].animate.set_opacity(0.3))
        # prior_save  = self.sliding_wins[prev_line]
        # self.play(ReplacementTransform(self.sliding_wins[prev_line], self.sliding_wins[line]))
        # self.play(self.sliding_wins[line].animate.set_opacity(0.3))
        # self.sliding_wins[prev_line] = prior_save
        self.play(self.sliding_wins[prev_line].animate.set_opacity(0))
        self.play(self.sliding_wins[line].animate.set_opacity(0.3))
