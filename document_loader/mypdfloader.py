from typing import List
from langchain.document_loaders.unstructured import UnstructuredFileLoader

class RapidOCRPDFLoader(UnstructuredFileLoader):
    def _get_elements(self) -> List:
        def pdf2text(filepath):
            import fitz
            from rapidocr_onnxruntime import RapidOCR
            import numpy as np
            ocr = RapidOCR()
            doc = fitz.open(filepath)
            resp = ""
            for page in doc:
                text = page.get_text("")
                resp += text + "\n"

                img_list = page.get_images()
                for img in img_list:
                    pix = fitz.Pixmap(doc, img[0])
                    img_array = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, 3)
                    result, _ = ocr(img_array)
                    ocr_result = [line[1] for line in result]
                    resp += "\n".join(ocr_result)
            return resp

        text = pdf2text(self.file_path)
        from unstructured.partition.text import partition_text
        return partition_text(text=text, **self.unstructured_kwargs)


if __name__ == "__main__":
    loader = UnstructuredRapidOCRPDFLoader(file_path="../docs/ocr_test.pdf")
    docs = loader.load()
    print(docs)
