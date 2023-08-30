import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image
from partidos import funcao_obter_filtro_usuario, funcao_normalizacao

class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Visualização de Dados Políticos")
        self.root.geometry("800x600")
        self.root.configure(bg="#E6F0F5")

        self.title_frame = tk.Frame(root, bg="#005A8C")
        self.title_frame.pack(fill=tk.X)  # Preenche a largura total

        self.title_label = tk.Label(self.title_frame, text="RELAÇÃO PARTIDOS E DEPUTADOS", bg="#005A8C", fg="white", font=("Helvetica", 18, "bold"))
        self.title_label.pack(pady=10)  # Espaço vertical abaixo do título

        self.frame = tk.Frame(root, bg="#E6F0F5")
        self.frame.pack(pady=15) 

        self.label_ano = tk.Label(root, text="Digite o ano:", bg="#E6F0F5")
        self.label_ano.pack()

        self.ano_entry = tk.Entry(root)
        self.ano_entry.pack()

        self.label_partidos = tk.Label(root, text="Digite os partidos (separados por vírgula) ou 'todos' para todos os partidos:", bg="#E6F0F5")
        self.label_partidos.pack()

        self.partidos_entry = tk.Entry(root)
        self.partidos_entry.pack()

        self.label_threshold = tk.Label(root, text="Digite o threshold:", bg="#E6F0F5")
        self.label_threshold.pack()

        self.threshold_entry = tk.Entry(root)
        self.threshold_entry.pack()

        self.generate_button = tk.Button(root, text="Gerar Visualização", command=self.generate_visualization, bg="#005A8C", fg="white", font=("Helvetica", 10, "bold"))
        self.generate_button.pack(pady=8)
        
        
        self.image_frame = tk.Frame(root)
        self.image_frame.pack()

        self.image_label_plotagem = tk.Label(self.image_frame)
        self.image_label_plotagem.pack(side=tk.LEFT, padx=10)  # Espaço horizontal entre as labels

        self.image_label_representacao = tk.Label(self.image_frame)
        self.image_label_representacao.pack(side=tk.LEFT, padx=10)

        self.image_label_heatmap = tk.Label(self.image_frame)
        self.image_label_heatmap.pack(side=tk.LEFT)

        self.empty_label = tk.Label(root, bg="#E6F0F5")
        self.empty_label.pack()

    def generate_visualization(self):
        ano = self.ano_entry.get()
        partidos_input = self.partidos_entry.get()

        if partidos_input.lower() == 'todos':
            partidos = []  # Lista vazia indica todos os partidos
        else:
            partidos = partidos_input.split(',')

        threshold = self.threshold_entry.get()

        funcao_normalizacao(partidos, ano, threshold)

        img_plotagem = Image.open("representacao_plotagem.png")
        img_plotagem.thumbnail((400, 400))
        img_plotagem = ImageTk.PhotoImage(img_plotagem)

        img_representacao = Image.open("representacao_grafico.png")
        img_representacao.thumbnail((400, 400))
        img_representacao = ImageTk.PhotoImage(img_representacao)

        img_heatmap = Image.open("heatmap.png")
        img_heatmap.thumbnail((400, 400))
        img_heatmap = ImageTk.PhotoImage(img_heatmap)

        self.image_label_plotagem.config(image=img_plotagem)
        self.image_label_plotagem.image = img_plotagem

        self.image_label_heatmap.config(image=img_heatmap)
        self.image_label_heatmap.image = img_heatmap

        self.image_label_representacao.config(image=img_representacao)
        self.image_label_representacao.image = img_representacao

if __name__ == "__main__":
    root = tk.Tk()
    gui = GUI(root)
    root.mainloop()




