from pdf2image import convert_from_path

# 1. 先强制输出无损 PNG；2. dpi 拉到 1200；3. 关闭一切压缩参数
pages = convert_from_path(
    './assets/teaser.pdf',
    dpi=1200,          # 关键：1200 dpi
    fmt='png',         # 关键：无损 PNG，不写就默认 JPEG
    thread_count=4,    # 加速，可选
    use_pdftocairo=True  # poppler 的 pdftocairo 路径，比 pdftoppm 更稳
)

# 只存封面
pages[0].save('./assets/teaser_max.png', format='PNG', compress_level=0)  # 0=无压缩