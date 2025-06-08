import os
import pandas as pd
import mysql.connector as mysqlc
from datetime import datetime
from dotenv import load_dotenv
import smtplib
from email.message import EmailMessage
from email.utils import make_msgid

load_dotenv()

class AgenteEmail:
    def __init__(self):
        self.conexao = mysqlc.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
        )
        self.emailRemetente = os.getenv("EMAIL_REMETENTE")
        self.senha = os.getenv("SENHA")

    def obterDados(self):
        sqlClientes = "SELECT id_cliente, nome, email FROM clientes"
        dfClientes = pd.read_sql(sqlClientes, self.conexao)
        
        sqlVendas = "SELECT id_cliente, data_venda FROM vendas"
        dfVendas = pd.read_sql(sqlVendas, self.conexao)
        
        return dfClientes, dfVendas
    
    def mandarEmail(self):
        dfClientes, dfVendas = self.obterDados()
        
        if dfVendas.empty:
            print("Nao foi encontrada nenhum venda")
            return

        dfComprasPorCliente = dfVendas.groupby('id_cliente').size().reset_index(name='totalVendas')
        
        dadosCompletos = pd.merge(dfClientes, dfComprasPorCliente, on='id_cliente', how='left')
        dadosCompletos['totalVendas'] = dadosCompletos['totalVendas'].fillna(0).astype(int)

        print("Analisando os clientes")
        
        for _, row in dadosCompletos.iterrows():
            totalVendas = row['totalVendas']
            emailCliente = row['email']
            nomeCliente = row['nome']

            if totalVendas >= 5:
                self._enviarEmailHtml(emailCliente, nomeCliente, tipo='cliente_ouro')
            elif 2 <= totalVendas < 5:
                self._enviarEmailHtml(emailCliente, nomeCliente, tipo='cliente_prata')
            elif totalVendas == 1:
                self._enviarEmailHtml(emailCliente, nomeCliente, tipo='cliente_bronze')

        print("Analise concluida")

    def _enviarEmailHtml(self, destinatario, nomeCliente, tipo):
        msg = EmailMessage()
        msg['Subject'] = "Uma novidade da Solus especialmente para você!"
        msg['From'] = self.emailRemetente
        msg['To'] = destinatario

        imageCid = make_msgid(domain='solus.com.br')

        if tipo == 'cliente_ouro':
            oferta = "Como um de nossos clientes mais valiosos, seu próximo pedido vem com um presente especial: um <strong>Carregador Solar Portátil EcoBoost</strong> por nossa conta! É a nossa forma de dizer obrigado."
            saudacao = f"Parabéns, {nomeCliente}! Você é um Cliente Ouro! 🥇"
        elif tipo == 'cliente_prata':
            oferta = "Agradecemos por sua confiança em nossos produtos! Para sua próxima compra, use o cupom <strong>SOLUS20</strong> e ganhe <strong>20% de desconto</strong> em qualquer item do nosso site."
            saudacao = f"Uma oferta especial para você, {nomeCliente}!"
        elif tipo == 'cliente_bronze':
            oferta = "Sentimos sua falta! Vimos que você já experimentou nossos produtos e queremos te convidar a continuar sua jornada sustentável. Use o cupom <strong>VOLTA15</strong> para ganhar <strong>15% de desconto e frete grátis</strong> no seu próximo pedido."
            saudacao = f"Olá, {nomeCliente}! Temos um convite para você."
        else:
            return

        corpoHtml = f"""
        <html>
        <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px; margin: 0; color: #333;">
            <div style="max-width: 600px; margin: auto; background-color: white; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 10px rgba(0,0,0,0.1);">
                <img src="cid:{imageCid[1:-1]}" style="width: 100%;" alt="Solus - Energia Sustentável">

                <div style="padding: 25px;">
                    <h2 style="color: #2c5b3c;">{saudacao}</h2>
                    <p style="color: #555; font-size: 16px; line-height: 1.6;">
                        {oferta}
                    </p>
                    <div style="text-align: center; margin: 30px 0;">
                        <a href="http://www.seusite.com.br" style="background-color: #4CAF50; color: white; padding: 12px 25px; text-decoration: none; border-radius: 5px; font-weight: bold;">Visitar a Loja</a>
                    </div>
                    <p style="font-size: 12px; color: #999; text-align: center;">Este é um e-mail automático, por favor não responda.</p>
                </div>
            </div>
        </body>
        </html>
        """
        msg.add_alternative(corpoHtml, subtype='html')

        try:
            with open('./assets/email_banner.png', 'rb') as imgFile:
                msg.get_payload()[0].add_related(imgFile.read(), 'image', 'png', cid=imageCid)
        except FileNotFoundError:
            print("A IMAGEM DE BANNER NAO FOI ENCOTRADA")
        except Exception as e:
            print(f"ERRO AO CARREGAR A IMAGEM {e}")

        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.login(self.emailRemetente, self.senha)
                smtp.send_message(msg)
            print(f"Email'{tipo}' foi enviado para {destinatario}")
        except Exception as e:
            print(f"Erro ao enviar e-mail para {destinatario}: {e}")

    def fecharConexao(self):
        if self.conexao and self.conexao.is_connected():
            self.conexao.close()
            print("CONEXAO BD ENCERRADA")