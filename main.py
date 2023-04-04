import tkinter

import gradio as gr
import gradio.themes
import openai
import tkinter

if __name__ == "__main__":
    openai.api_key = "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"
    
    message = [{"role": "system", "content": "You are a helpful and kind AI Assistant."}]
    tk = tkinter.Tk()
    height = tk.winfo_height()
    tk.quit()
    
    
    def chat_bot(_input):
        if _input:
            message.append({"role": "user", "content": _input})
            chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=message)
            reply = chat.choices[0].message.content
            message.append({"role": "assistant", "content": reply})
            return reply
    
    
    with gr.Blocks(theme=gr.themes.Monochrome(
            neutral_hue='blue',
    )) as interface:
        
        """ 单次询问模式 """
        # with gr.Row():
        #     inputs = gr.inputs.Textbox(lines=7, label="你")
        #     outputs = gr.outputs.Textbox(label="AI")
        #
        # btn = gr.Button(value="提交")
        # btn.click(fn=chat_bot, inputs=[inputs], outputs=[outputs])
        
        """ 聊天对话框模式 """
        chatbot = gr.Chatbot(label="Yo-i Bot")
        with gr.Row():
            with gr.Column(scale=80):
                msg = gr.Textbox(label="你", lines=1)
            with gr.Column(scale=20, min_width=0):
                submit_btn = gr.Button('发送')
                clear_btn = gr.Button('清除聊天内容')
        
        
        def user(user_message, history):
            return "", history + [[user_message, None]]
        
        
        def bot(history):
            user_msg = history[-1][0]
            print(user_msg)
            bot_reply = chat_bot(user_msg)
            history[-1][1] = bot_reply
            return history
        
        
        def sub(user_message, history):
            _, history = user(user_message, history)
            msg.value = None
            return bot(history)
        
        
        clear_btn.click(lambda: None, None, chatbot, queue=False)
        submit_btn.click(fn=sub, inputs=[msg, chatbot], outputs=[chatbot])
        submit_btn.click(lambda x: gr.update(value=''), [], [msg])
        msg.submit(user, [msg, chatbot], [msg, chatbot], queue=False).then(bot, chatbot, chatbot)
    
    interface.title = "Yo-i GPT"
    interface.launch(server_port=9000)
