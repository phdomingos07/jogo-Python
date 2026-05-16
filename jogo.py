
import pygame

# ---------------- Inicialização ----------------
pygame.init()

tamanho_tela = (600, 600)
tela = pygame.display.set_mode(tamanho_tela)
pygame.display.set_caption("Brick Breaker")

tamanho_bola = 10
bola = pygame.Rect(100, 500, tamanho_bola, tamanho_bola)

tamanho_Jogador = 100
jogador = pygame.Rect(200, 570, tamanho_Jogador, 10)

qtdeBlocosLinha = 5
qtdeLinhas = 3

cores = {
    "branca": (255, 255, 255),
    "preto": (0, 0, 0),
    "azul": (0, 0, 255),
    "amarelo": (255, 255, 0),
    "verde": (0, 255, 0),
    "vermelho": (255, 0, 0)
}

clock = pygame.time.Clock()

# estados
fimJogo = False
estado = "menu"
dificuldade = "medio"

movBola = [6, -6]

# ---------------- Funções ----------------

def telaInicial():
    tela.fill(cores["preto"])

    fonte_titulo = pygame.font.Font(None, 60)
    fonte_opcao = pygame.font.Font(None, 30)

    titulo = fonte_titulo.render("BRICK BREAKER", True, cores["branca"])
    tela.blit(titulo, (150, 50))

    tela.blit(fonte_opcao.render("1 - Fácil", True, cores["verde"]), (200, 250))
    tela.blit(fonte_opcao.render("2 - Médio", True, cores["amarelo"]), (200, 300))
    tela.blit(fonte_opcao.render("3 - Difícil", True, cores["vermelho"]), (200, 350))

    tela.blit(fonte_opcao.render("ENTER para começar", True, cores["branca"]), (170, 450))


def criarBlocos():
    blocos = []
    larguraTela = tamanho_tela[0]

    larguraBloco = larguraTela / qtdeBlocosLinha - 5
    alturaBloco = 15

    for j in range(qtdeLinhas):
        for i in range(qtdeBlocosLinha):
            bloco = pygame.Rect(
                i * (larguraBloco + 5),
                j * (alturaBloco + 10),
                larguraBloco,
                alturaBloco
            )
            blocos.append(bloco)

    return blocos


def desenharItens():
    tela.fill(cores["preto"])
    pygame.draw.rect(tela, cores["amarelo"], jogador)
    pygame.draw.rect(tela, cores["branca"], bola)


def desenharBlocos():
    for bloco in blocos:
        pygame.draw.rect(tela, cores["azul"], bloco)


def desenharPontuacao():
    pontos = total_blocos - len(blocos)
    fonte = pygame.font.Font(None, 30)
    texto = fonte.render(f"Pontos: {pontos}", True, cores["branca"])
    tela.blit(texto, (10, 570))


def desenharGameOver():
    fonte = pygame.font.Font(None, 60)
    texto = fonte.render("GAME OVER", True, cores["vermelho"])
    tela.blit(texto, (160, 280))

    fonte2 = pygame.font.Font(None, 30)
    texto2 = fonte2.render("Pressione R para reiniciar", True, cores["branca"])
    tela.blit(texto2, (170, 350))


def desenharVitoria():
    fonte = pygame.font.Font(None, 60)
    texto = fonte.render("VOCÊ GANHOU!", True, cores["verde"])
    tela.blit(texto, (120, 280))

    fonte2 = pygame.font.Font(None, 30)
    texto2 = fonte2.render("Pressione R para reiniciar", True, cores["branca"])
    tela.blit(texto2, (170, 350))


def movimentoJogador():
    teclas = pygame.key.get_pressed()

    if (teclas[pygame.K_RIGHT] or teclas[pygame.K_d]) and jogador.right < tamanho_tela[0]:
        jogador.x += 6
    if (teclas[pygame.K_LEFT] or teclas[pygame.K_a]) and jogador.left > 0:
        jogador.x -= 6


def movimentoBola():
    global movBola

    bola.x += movBola[0]
    bola.y += movBola[1]

    # paredes
    if bola.left <= 0 or bola.right >= tamanho_tela[0]:
        movBola[0] *= -1

    if bola.top <= 0:
        movBola[1] *= -1

    # jogador (ângulo)
    if jogador.colliderect(bola) and movBola[1] > 0:
        impacto = bola.centerx - jogador.centerx
        impacto /= (tamanho_Jogador / 2)

        velocidade = abs(movBola[1])
        movBola[0] = impacto * velocidade
        movBola[1] = -abs(velocidade)

        bola.bottom = jogador.top

    # blocos
    for bloco in blocos[:]:
        if bloco.colliderect(bola):
            blocos.remove(bloco)

            movBola[1] *= -1

            if movBola[1] > 0:
                bola.top = bloco.bottom
            else:
                bola.bottom = bloco.top

            break

    # chão
    if bola.bottom >= tamanho_tela[1]:
        return False

    return True


def reiniciarJogo():
    global bola, jogador, blocos, movBola, estado

    bola.x = 100
    bola.y = 500
    jogador.x = 200

    blocos = criarBlocos()

    if dificuldade == "facil":
        movBola = [4, -4]
    elif dificuldade == "medio":
        movBola = [6, -6]
    else:
        movBola = [11, -11]

    estado = "menu"


# ---------------- Execução ----------------

blocos = criarBlocos()
total_blocos = len(blocos)

while not fimJogo:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            fimJogo = True

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_r and estado in ["gameover", "vitoria"]:
                reiniciarJogo()

        if estado == "menu" and evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_1:
                dificuldade = "facil"
            if evento.key == pygame.K_2:
                dificuldade = "medio"
            if evento.key == pygame.K_3:
                dificuldade = "dificil"

            if evento.key == pygame.K_RETURN:
                if dificuldade == "facil":
                    movBola = [4, -4]
                elif dificuldade == "medio":
                    movBola = [6, -6]
                else:
                    movBola = [11, -11]

                estado = "jogando"

    if estado == "menu":
        telaInicial()

    elif estado == "jogando":
        movimentoJogador()

        if not movimentoBola():
            estado = "gameover"

        desenharItens()
        desenharBlocos()
        desenharPontuacao()

        if len(blocos) == 0:
            estado = "vitoria"

    elif estado == "gameover":
        desenharGameOver()

    elif estado == "vitoria":
        desenharVitoria()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()