# Mood Flow

O Mood Flow é um sistema de reprodução musical desenvolvido em Python com foco na aplicação prática dos conceitos estudados nas disciplinas de Programação Orientada a Objetos e Estrutura de Dados. O projeto permite organizar e reproduzir músicas armazenadas localmente no computador, utilizando uma estrutura baseada em playlists organizadas por pastas. Cada pasta é interpretada pelo sistema como uma playlist, possibilitando que novas músicas sejam adicionadas sem necessidade de alterações no código.

Ao iniciar o programa, a biblioteca musical é carregada automaticamente a partir da pasta configurada pelo usuário. Todas as músicas encontradas são transformadas em objetos da classe Musica e armazenadas em uma biblioteca implementada por meio de uma lista encadeada. Dessa forma, o sistema consegue percorrer, listar e organizar os dados sem depender de listas nativas do Python como estrutura principal de armazenamento.

A reprodução das músicas é controlada por uma fila FIFO (First In, First Out), garantindo que a ordem de execução siga a sequência em que os elementos foram adicionados. Além disso, o sistema mantém um histórico das músicas reproduzidas, permitindo ao usuário consultar posteriormente quais faixas já foram executadas.

A arquitetura do projeto foi organizada em diferentes módulos, cada um com uma responsabilidade específica. A classe Musica representa os dados de cada arquivo musical. A classe Biblioteca é responsável pelo armazenamento das músicas em lista encadeada. As classes NodoLista e NodoFila representam os nós utilizados nas estruturas de dados. A classe Fila controla a ordem de reprodução. O módulo Leitor realiza a leitura automática das pastas e arquivos presentes no disco. O módulo Player é responsável pela comunicação com o VLC para reprodução de áudio e vídeo. O Controlador centraliza a lógica do sistema e a Interface realiza a interação com o usuário através do terminal.

Entre as principais funcionalidades implementadas estão o carregamento automático de playlists, reprodução de músicas locais, visualização da biblioteca completa, exibição das playlists disponíveis, reprodução de playlists inteiras, reprodução de músicas individuais, adição de músicas à fila de execução, atualização dinâmica da biblioteca e consulta ao histórico de reprodução.

Para o funcionamento correto do sistema, as músicas devem estar organizadas dentro da pasta playlist, sendo que cada subpasta representa uma playlist diferente. O sistema suporta diversos formatos de áudio e vídeo, incluindo MP3, MP4, WAV, FLAC, OGG, AAC, MKV e WEBM. A reprodução é realizada por meio da biblioteca python-vlc.

Este projeto foi desenvolvido com o objetivo de consolidar conhecimentos de Programação Orientada a Objetos, listas encadeadas, filas FIFO, modularização de código e separação de responsabilidades, demonstrando na prática a aplicação desses conceitos em um sistema funcional de gerenciamento e reprodução musical.
