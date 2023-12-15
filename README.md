Функція def graph_coloring(graph) створена для розфарбування графу в три кольори так, аби дві суміжні вершини мали різний колір.
Для цієї реалізації використовується під фукнція def color(lst), яка має сет, куди записується використаний колір і має визначені 3 кольори,
які будуть потрібно для реалізації. Для вибору, який колір можна використати існує перевірка, і якщо це можливо то вибирає доступний.
Далі функція проходиться по всіх вершинах і якщо колір підходить, бо він ще не використаний, то додає до вершини його. Якщо це неможливо,
вертається повідомлення "Неможливо розфарбувати".
<img width="976" alt="Screenshot 2023-12-15 at 1 02 50 PM" src="https://github.com/shshrg/graphetc/assets/149332573/4cd2e097-5d8e-4a56-a03b-88fa36df8f6f">

Для реалізації використовувалось означення:

<img width="470" alt="Screenshot 2023-12-15 at 1 01 31 PM" src="https://github.com/shshrg/graphetc/assets/149332573/637f9a2f-bc21-4cbf-85fe-bff69afb5a4f">
