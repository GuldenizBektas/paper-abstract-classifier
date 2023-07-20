def relabel(predicted : int) -> str:

    labels = {0: "Artifical Intelligence",
              1: "Computer Vision",
              2: "Data Structures and Algorithms",
              3: "Machine Learning"}

    return labels[predicted]