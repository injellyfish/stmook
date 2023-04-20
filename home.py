import streamlit as st
import pandas as pd
import numpy as np
import tempfile
from PyPDF2 import PdfReader, PdfWriter

pwrite = PdfWriter()

st.title("📖线装书页码自动排序")

st.markdown("""
    这是自制锁线装订书的辅助工具，用于实现 PDF 文件中页码的自动排序。
""")

st.markdown("""
    ### 1️⃣ 上传 PDF 文件
""")

uploaded_file = st.file_uploader("⚠️请注意：您的文件页数需要是 4 的倍数！", type=['pdf'])

if uploaded_file is not None:
    pread = PdfReader(uploaded_file)
    numpages = len(pread.pages)

    if numpages%4 == 0:

        st.write('✅上传成功！您的文件一共有 ' + str(numpages) + ' 页，组合如下：')

        count = 2
        p4 = int(numpages/4)

        while count <= p4/2+1:
            if p4 % count == 0:         
                p4a = int(p4/count)
                p4a4 = p4a*4
                st.markdown("- "+str(count)+" 份书帖，每份纸张数 "+str(p4a)+"，每份页数 "+str(p4a4))
                count = count + 1
            else:
                count = count + 1


        st.markdown("---")

        st.markdown("""
            ### 2️⃣ 设置每份书帖页数

            这里页数计算方式为`每份书帖中纸张数 × 4`。
            
            例如：假设每份书帖由 3 张纸组成，则每份书帖有 3×4=12 页。
        """)


        num = st.text_input('请输入每份书帖的页数（需是4的倍数）：')
        if num:
            if int(num)%4 == 0:

                sp = int(num)
                cp = numpages/sp
                cs = int(cp)
                pl = int(sp/4)
                k = 0

                for i in range(0,cs):      
                    z = 1
                    y = 0
                    
                    for w in range(0,pl):        
                        pageObj1 = pread.pages[sp*k+sp-z]
                        pwrite.add_page(pageObj1)
                        
                        pageObj2 = pread.pages[sp*k+y]
                        pwrite.add_page(pageObj2)
                        
                        pageObj3 = pread.pages[sp*k+z]
                        pwrite.add_page(pageObj3)
                        
                        pageObj4 = pread.pages[sp*k+sp-y-2] 
                        pwrite.add_page(pageObj4)
                                        
                        if w == pl:
                            z = 1
                            y = 0
                        else:
                            z = z+2
                            y = y+2
                    k = k+1  

                st.write("✅处理完成！每份书帖有 ",str(sp)," 页")

                st.markdown("---")

                st.markdown("""
                    ### 3️⃣ 最后一步
                """)

                name = st.text_input('请输入处理完成后 PDF 文件名：')

                if name:
                    fp = tempfile.NamedTemporaryFile(delete=True)
                    try:
                        pwrite.write(open(fp.name + ".pdf", 'wb'))
                    

                        with open(fp.name + ".pdf", 'rb') as pdf_file:
                            st.download_button(
                                label = "📥下载",
                                data = pdf_file,
                                file_name = name + ".pdf",
                                mime = "application/pdf"
                            )
                    finally:
                        fp.close()
            else:
                st.markdown("⛔啊哦，PDF 页数需是 4 的倍数，请再调整下吧！")


    else:
        st.markdown("⛔啊哦，PDF 页数需是 4 的倍数，请再调整下吧！")
