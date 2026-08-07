---
title: "Amostras de audio da dissertacao"
permalink: /amostras/
layout: default
---

<!-- ARQUIVO GERADO AUTOMATICAMENTE -- nao edite a mao.
     Fonte: docs/amostras/manifest.json
     Regerar: python docs/amostras/montar_manifesto.py
              python docs/amostras/gerar_pagina.py -->

<style>
  .wrapper, .markdown-body, .inner, #main_content {
    max-width: 1100px !important;
    padding: 1rem 1.5rem !important;
  }
  .art-intro { font-size: 1rem; line-height: 1.6; }
  .art-meta {
    border: 1px solid #d6d6d6; border-radius: 6px;
    padding: 0.75rem 1rem; margin: 1.25rem 0;
    background: #fafafa; font-size: 0.9rem; line-height: 1.7;
  }
  .art-meta dt { font-weight: 600; }
  .art-sumario { margin: 1.5rem 0 2.5rem; padding: 0; list-style: none; }
  .art-sumario li {
    padding: 0.35rem 0; border-bottom: 1px solid #ececec; font-size: 0.95rem;
  }
  .art-sumario .art-num {
    display: inline-block; min-width: 1.8rem; font-weight: 600; color: #666;
  }
  .art-bloco { margin: 3rem 0; padding-top: 1rem; border-top: 2px solid #e0e0e0; }
  .art-bloco h2 { margin-bottom: 0.35rem; }
  .art-selo {
    display: inline-block; font-size: 0.72rem; text-transform: uppercase;
    letter-spacing: 0.04em; padding: 0.18rem 0.5rem; border-radius: 3px;
    border: 1px solid currentColor; vertical-align: middle; margin-left: 0.5rem;
  }
  .art-selo--pos  { color: #1d6f42; }
  .art-selo--parc { color: #8a6100; }
  .art-selo--neg  { color: #9a2b2b; }
  .art-selo--ref  { color: #40566d; }
  .art-afirmacao {
    border-left: 4px solid #999; padding: 0.5rem 0 0.5rem 0.9rem;
    margin: 0.9rem 0 1rem; font-size: 0.95rem; background: #f7f7f7;
  }
  .art-afirmacao strong { display: block; font-size: 0.75rem;
    text-transform: uppercase; letter-spacing: 0.04em; color: #666;
    margin-bottom: 0.25rem; }
  .art-desc { font-size: 0.95rem; line-height: 1.65; }
  .art-tabela { margin: 1.75rem 0; }
  .art-tabela > h3 { font-size: 1.02rem; margin-bottom: 0.3rem; }
  .art-nota { font-size: 0.87rem; color: #555; margin: 0 0 0.9rem; line-height: 1.55; }
  .art-linha {
    border: 1px solid #e2e2e2; border-radius: 6px;
    padding: 0.8rem 0.9rem; margin-bottom: 0.7rem; background: #fff;
  }
  .art-rotulo-linha {
    font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.04em;
    color: #777; margin: 0 0 0.3rem;
  }
  .art-texto {
    margin: 0 0 0.7rem; font-size: 0.93rem; line-height: 1.5; color: #222;
  }
  .art-texto::before { content: "\201C"; }
  .art-texto::after  { content: "\201D"; }
  .art-cols { display: flex; flex-wrap: wrap; gap: 0.75rem; }
  .art-col { flex: 1 1 220px; min-width: 200px; }
  .art-col-rot {
    display: block; font-size: 0.78rem; font-weight: 600; color: #444;
    margin-bottom: 0.25rem;
  }
  .art-col audio { width: 100%; max-width: 100%; height: 36px; }
  .art-vazio {
    display: block; font-size: 0.8rem; color: #999; font-style: italic;
    padding: 0.55rem 0;
  }
  .art-links { margin: 1.25rem 0 0; padding: 0; list-style: none; font-size: 0.93rem; }
  .art-links li { padding: 0.2rem 0; }
  .art-topo { font-size: 0.82rem; color: #777; }
  .art-rodape {
    margin-top: 3rem; padding-top: 1rem; border-top: 1px solid #e5e5e5;
    font-size: 0.88rem; color: #555; line-height: 1.65;
  }
  @media (max-width: 640px) {
    .wrapper, .markdown-body, .inner, #main_content { padding: 0.75rem !important; }
    .art-col { flex: 1 1 100%; min-width: 0; }
  }
</style>

# Amostras de audio da dissertacao

<p class="art-intro">Material de escuta para verificacao das afirmacoes feitas nos capitulos de resultados. Todos os audios tocam diretamente no navegador, sem instalacao e sem login. Cada bloco abaixo corresponde a uma afirmacao feita na dissertacao e reune o material necessario para confirma-la -- inclusive quando o resultado e negativo.</p>

<dl class="art-meta">
<dt>Corpus de adaptacao</dt><dd>FALA_PB -- aproximadamente 111 h de fala com sotaque paraibano</dd>
<dt>Modelos investigados</dt><dd>XTTS, F5-TTS, Orpheus TTS, Fish Speech, Qwen3-TTS</dd>
<dt>Estrategias de adaptacao</dt><dd>Clonagem de fala, Ajuste fino, Treinamento a partir de pesos aleatorios</dd>
<dt>Audios nesta pagina</dt><dd>175</dd>
</dl>

## Sumario

<ul class="art-sumario" id="sumario">
<li><span class="art-num">1.</span><a href="#clonagem">Clonagem de fala (XTTS)</a><span class="art-selo art-selo--neg">resultado negativo</span></li>
<li><span class="art-num">2.</span><a href="#xtts-ajuste-fino">XTTS -- ajuste fino</a><span class="art-selo art-selo--pos">resultado positivo</span></li>
<li><span class="art-num">3.</span><a href="#f5tts-ajuste-fino">F5-TTS -- ajuste fino</a><span class="art-selo art-selo--neg">resultado negativo</span></li>
<li><span class="art-num">4.</span><a href="#orpheus-ajuste-fino">Orpheus TTS -- ajuste fino</a><span class="art-selo art-selo--pos">resultado positivo</span></li>
<li><span class="art-num">5.</span><a href="#fishspeech-ajuste-fino">Fish Speech -- ajuste fino</a><span class="art-selo art-selo--pos">resultado positivo</span></li>
<li><span class="art-num">6.</span><a href="#qwen3-ajuste-fino">Qwen3-TTS -- ajuste fino</a><span class="art-selo art-selo--neg">resultado negativo</span></li>
<li><span class="art-num">7.</span><a href="#f5tts-do-zero">F5-TTS treinado a partir de pesos aleatorios</a><span class="art-selo art-selo--neg">resultado negativo</span></li>
<li><span class="art-num">8.</span><a href="#avaliacao-automatica">Avaliacao automatica -- conjunto completo</a><span class="art-selo art-selo--ref">conjunto de referencia</span></li>
</ul>

<section class="art-bloco" id="clonagem" markdown="0">
<h2>1. Clonagem de fala (XTTS)<span class="art-selo art-selo--neg">resultado negativo</span></h2>
<p class="art-topo">Estrategia: Clonagem de fala &middot; <a href="#sumario">voltar ao sumario</a></p>
<div class="art-afirmacao"><strong>Afirmacao verificavel</strong>O timbre do locutor e reproduzido de forma reconhecivel, mas o sotaque paraibano nao e capturado em nenhuma das tres condicoes de referencia (10 s, 30 s e 60 s).</div>
<p class="art-desc">O que se espera ouvir: uma voz que soa como a do locutor de referencia, porem com prosodia e realizacao fonetica de padrao sudeste/neutro. Alongar a referencia de 10 s para 60 s melhora pouco ou nada a transferencia de sotaque -- e este e o ponto do bloco. Pagina completa do experimento: <a href="/fala_pb/2/">reuniao 2</a>.</p>
<div class="art-tabela">
<h3>Referencia de 10 s</h3>
<p class="art-nota">Cinco gravacoes de referencia de aproximadamente 10 s cada, ao lado da sintese produzida com o mesmo texto da referencia. Compare timbre (proximo) e sotaque (distante).</p>
<div class="art-linha">
<p class="art-rotulo-linha">Amostra 1</p>
<div class="art-cols">
<div class="art-col">
<span class="art-col-rot">Referencia (locutor real)</span>
<audio controls preload="none" src="/fala_pb/audios/experimento_timbre/refs/thomaz_a1.wav"><a href="/fala_pb/audios/experimento_timbre/refs/thomaz_a1.wav">baixar audio</a></audio>
</div>
<div class="art-col">
<span class="art-col-rot">Sintese clonada (mesmo texto)</span>
<audio controls preload="none" src="/fala_pb/audios/experimento_timbre/output%20texto%20original/xtts_A1.wav"><a href="/fala_pb/audios/experimento_timbre/output%20texto%20original/xtts_A1.wav">baixar audio</a></audio>
</div>
</div></div>
<div class="art-linha">
<p class="art-rotulo-linha">Amostra 2</p>
<div class="art-cols">
<div class="art-col">
<span class="art-col-rot">Referencia (locutor real)</span>
<audio controls preload="none" src="/fala_pb/audios/experimento_timbre/refs/thomaz_a2.wav"><a href="/fala_pb/audios/experimento_timbre/refs/thomaz_a2.wav">baixar audio</a></audio>
</div>
<div class="art-col">
<span class="art-col-rot">Sintese clonada (mesmo texto)</span>
<audio controls preload="none" src="/fala_pb/audios/experimento_timbre/output%20texto%20original/xtts_A2.wav"><a href="/fala_pb/audios/experimento_timbre/output%20texto%20original/xtts_A2.wav">baixar audio</a></audio>
</div>
</div></div>
<div class="art-linha">
<p class="art-rotulo-linha">Amostra 3</p>
<div class="art-cols">
<div class="art-col">
<span class="art-col-rot">Referencia (locutor real)</span>
<audio controls preload="none" src="/fala_pb/audios/experimento_timbre/refs/thomaz_a3.wav"><a href="/fala_pb/audios/experimento_timbre/refs/thomaz_a3.wav">baixar audio</a></audio>
</div>
<div class="art-col">
<span class="art-col-rot">Sintese clonada (mesmo texto)</span>
<audio controls preload="none" src="/fala_pb/audios/experimento_timbre/output%20texto%20original/xtts_A3.wav"><a href="/fala_pb/audios/experimento_timbre/output%20texto%20original/xtts_A3.wav">baixar audio</a></audio>
</div>
</div></div>
<div class="art-linha">
<p class="art-rotulo-linha">Amostra 4</p>
<div class="art-cols">
<div class="art-col">
<span class="art-col-rot">Referencia (locutor real)</span>
<audio controls preload="none" src="/fala_pb/audios/experimento_timbre/refs/thomaz_a4.wav"><a href="/fala_pb/audios/experimento_timbre/refs/thomaz_a4.wav">baixar audio</a></audio>
</div>
<div class="art-col">
<span class="art-col-rot">Sintese clonada (mesmo texto)</span>
<audio controls preload="none" src="/fala_pb/audios/experimento_timbre/output%20texto%20original/xtts_A4.wav"><a href="/fala_pb/audios/experimento_timbre/output%20texto%20original/xtts_A4.wav">baixar audio</a></audio>
</div>
</div></div>
<div class="art-linha">
<p class="art-rotulo-linha">Amostra 5</p>
<div class="art-cols">
<div class="art-col">
<span class="art-col-rot">Referencia (locutor real)</span>
<audio controls preload="none" src="/fala_pb/audios/experimento_timbre/refs/thomaz_a5.wav"><a href="/fala_pb/audios/experimento_timbre/refs/thomaz_a5.wav">baixar audio</a></audio>
</div>
<div class="art-col">
<span class="art-col-rot">Sintese clonada (mesmo texto)</span>
<audio controls preload="none" src="/fala_pb/audios/experimento_timbre/output%20texto%20original/xtts_A5.wav"><a href="/fala_pb/audios/experimento_timbre/output%20texto%20original/xtts_A5.wav">baixar audio</a></audio>
</div>
</div></div>
</div>
<div class="art-tabela">
<h3>Referencia de 30 s</h3>
<p class="art-nota">Cinco gravacoes de referencia de aproximadamente 30 s cada, ao lado da sintese produzida com o mesmo texto da referencia. Compare timbre (proximo) e sotaque (distante).</p>
<div class="art-linha">
<p class="art-rotulo-linha">Amostra 1</p>
<div class="art-cols">
<div class="art-col">
<span class="art-col-rot">Referencia (locutor real)</span>
<audio controls preload="none" src="/fala_pb/audios/experimento_timbre/refs/thomaz_b1.wav"><a href="/fala_pb/audios/experimento_timbre/refs/thomaz_b1.wav">baixar audio</a></audio>
</div>
<div class="art-col">
<span class="art-col-rot">Sintese clonada (mesmo texto)</span>
<audio controls preload="none" src="/fala_pb/audios/experimento_timbre/output%20texto%20original/xtts_B1.wav"><a href="/fala_pb/audios/experimento_timbre/output%20texto%20original/xtts_B1.wav">baixar audio</a></audio>
</div>
</div></div>
<div class="art-linha">
<p class="art-rotulo-linha">Amostra 2</p>
<div class="art-cols">
<div class="art-col">
<span class="art-col-rot">Referencia (locutor real)</span>
<audio controls preload="none" src="/fala_pb/audios/experimento_timbre/refs/thomaz_b2.wav"><a href="/fala_pb/audios/experimento_timbre/refs/thomaz_b2.wav">baixar audio</a></audio>
</div>
<div class="art-col">
<span class="art-col-rot">Sintese clonada (mesmo texto)</span>
<audio controls preload="none" src="/fala_pb/audios/experimento_timbre/output%20texto%20original/xtts_B2.wav"><a href="/fala_pb/audios/experimento_timbre/output%20texto%20original/xtts_B2.wav">baixar audio</a></audio>
</div>
</div></div>
<div class="art-linha">
<p class="art-rotulo-linha">Amostra 3</p>
<div class="art-cols">
<div class="art-col">
<span class="art-col-rot">Referencia (locutor real)</span>
<audio controls preload="none" src="/fala_pb/audios/experimento_timbre/refs/thomaz_b3.wav"><a href="/fala_pb/audios/experimento_timbre/refs/thomaz_b3.wav">baixar audio</a></audio>
</div>
<div class="art-col">
<span class="art-col-rot">Sintese clonada (mesmo texto)</span>
<audio controls preload="none" src="/fala_pb/audios/experimento_timbre/output%20texto%20original/xtts_B3.wav"><a href="/fala_pb/audios/experimento_timbre/output%20texto%20original/xtts_B3.wav">baixar audio</a></audio>
</div>
</div></div>
<div class="art-linha">
<p class="art-rotulo-linha">Amostra 4</p>
<div class="art-cols">
<div class="art-col">
<span class="art-col-rot">Referencia (locutor real)</span>
<audio controls preload="none" src="/fala_pb/audios/experimento_timbre/refs/thomaz_b4.wav"><a href="/fala_pb/audios/experimento_timbre/refs/thomaz_b4.wav">baixar audio</a></audio>
</div>
<div class="art-col">
<span class="art-col-rot">Sintese clonada (mesmo texto)</span>
<audio controls preload="none" src="/fala_pb/audios/experimento_timbre/output%20texto%20original/xtts_B4.wav"><a href="/fala_pb/audios/experimento_timbre/output%20texto%20original/xtts_B4.wav">baixar audio</a></audio>
</div>
</div></div>
<div class="art-linha">
<p class="art-rotulo-linha">Amostra 5</p>
<div class="art-cols">
<div class="art-col">
<span class="art-col-rot">Referencia (locutor real)</span>
<audio controls preload="none" src="/fala_pb/audios/experimento_timbre/refs/thomaz_b5.wav"><a href="/fala_pb/audios/experimento_timbre/refs/thomaz_b5.wav">baixar audio</a></audio>
</div>
<div class="art-col">
<span class="art-col-rot">Sintese clonada (mesmo texto)</span>
<audio controls preload="none" src="/fala_pb/audios/experimento_timbre/output%20texto%20original/xtts_B5.wav"><a href="/fala_pb/audios/experimento_timbre/output%20texto%20original/xtts_B5.wav">baixar audio</a></audio>
</div>
</div></div>
</div>
<div class="art-tabela">
<h3>Referencia de 60 s</h3>
<p class="art-nota">Cinco gravacoes de referencia de aproximadamente 60 s cada, ao lado da sintese produzida com o mesmo texto da referencia. Compare timbre (proximo) e sotaque (distante).</p>
<div class="art-linha">
<p class="art-rotulo-linha">Amostra 1</p>
<div class="art-cols">
<div class="art-col">
<span class="art-col-rot">Referencia (locutor real)</span>
<audio controls preload="none" src="/fala_pb/audios/experimento_timbre/refs/thomaz_c1.wav"><a href="/fala_pb/audios/experimento_timbre/refs/thomaz_c1.wav">baixar audio</a></audio>
</div>
<div class="art-col">
<span class="art-col-rot">Sintese clonada (mesmo texto)</span>
<audio controls preload="none" src="/fala_pb/audios/experimento_timbre/output%20texto%20original/xtts_C1.wav"><a href="/fala_pb/audios/experimento_timbre/output%20texto%20original/xtts_C1.wav">baixar audio</a></audio>
</div>
</div></div>
<div class="art-linha">
<p class="art-rotulo-linha">Amostra 2</p>
<div class="art-cols">
<div class="art-col">
<span class="art-col-rot">Referencia (locutor real)</span>
<audio controls preload="none" src="/fala_pb/audios/experimento_timbre/refs/thomaz_c2.wav"><a href="/fala_pb/audios/experimento_timbre/refs/thomaz_c2.wav">baixar audio</a></audio>
</div>
<div class="art-col">
<span class="art-col-rot">Sintese clonada (mesmo texto)</span>
<audio controls preload="none" src="/fala_pb/audios/experimento_timbre/output%20texto%20original/xtts_C2.wav"><a href="/fala_pb/audios/experimento_timbre/output%20texto%20original/xtts_C2.wav">baixar audio</a></audio>
</div>
</div></div>
<div class="art-linha">
<p class="art-rotulo-linha">Amostra 3</p>
<div class="art-cols">
<div class="art-col">
<span class="art-col-rot">Referencia (locutor real)</span>
<audio controls preload="none" src="/fala_pb/audios/experimento_timbre/refs/thomaz_c3.wav"><a href="/fala_pb/audios/experimento_timbre/refs/thomaz_c3.wav">baixar audio</a></audio>
</div>
<div class="art-col">
<span class="art-col-rot">Sintese clonada (mesmo texto)</span>
<audio controls preload="none" src="/fala_pb/audios/experimento_timbre/output%20texto%20original/xtts_C3.wav"><a href="/fala_pb/audios/experimento_timbre/output%20texto%20original/xtts_C3.wav">baixar audio</a></audio>
</div>
</div></div>
<div class="art-linha">
<p class="art-rotulo-linha">Amostra 4</p>
<div class="art-cols">
<div class="art-col">
<span class="art-col-rot">Referencia (locutor real)</span>
<audio controls preload="none" src="/fala_pb/audios/experimento_timbre/refs/thomaz_c4.wav"><a href="/fala_pb/audios/experimento_timbre/refs/thomaz_c4.wav">baixar audio</a></audio>
</div>
<div class="art-col">
<span class="art-col-rot">Sintese clonada (mesmo texto)</span>
<audio controls preload="none" src="/fala_pb/audios/experimento_timbre/output%20texto%20original/xtts_C4.wav"><a href="/fala_pb/audios/experimento_timbre/output%20texto%20original/xtts_C4.wav">baixar audio</a></audio>
</div>
</div></div>
<div class="art-linha">
<p class="art-rotulo-linha">Amostra 5</p>
<div class="art-cols">
<div class="art-col">
<span class="art-col-rot">Referencia (locutor real)</span>
<audio controls preload="none" src="/fala_pb/audios/experimento_timbre/refs/thomaz_c5.wav"><a href="/fala_pb/audios/experimento_timbre/refs/thomaz_c5.wav">baixar audio</a></audio>
</div>
<div class="art-col">
<span class="art-col-rot">Sintese clonada (mesmo texto)</span>
<audio controls preload="none" src="/fala_pb/audios/experimento_timbre/output%20texto%20original/xtts_C5.wav"><a href="/fala_pb/audios/experimento_timbre/output%20texto%20original/xtts_C5.wav">baixar audio</a></audio>
</div>
</div></div>
</div>
<div class="art-tabela">
<h3>Dez frases-chave, nas tres duracoes de referencia</h3>
<p class="art-nota">As mesmas dez frases sintetizadas a partir das referencias de 10 s, 30 s e 60 s. Aumentar a duracao da referencia nao aproxima a saida do sotaque paraibano.</p>
<div class="art-linha">
<p class="art-texto">A tecnologia mudou a forma como nos comunicamos e aprendemos.</p>
<div class="art-cols">
<div class="art-col">
<span class="art-col-rot">Referencia de 10 s</span>
<audio controls preload="none" src="/fala_pb/audios/experimento_timbre/output/xtts_A1.wav"><a href="/fala_pb/audios/experimento_timbre/output/xtts_A1.wav">baixar audio</a></audio>
</div>
<div class="art-col">
<span class="art-col-rot">Referencia de 30 s</span>
<audio controls preload="none" src="/fala_pb/audios/experimento_timbre/output/xtts_B1.wav"><a href="/fala_pb/audios/experimento_timbre/output/xtts_B1.wav">baixar audio</a></audio>
</div>
<div class="art-col">
<span class="art-col-rot">Referencia de 60 s</span>
<audio controls preload="none" src="/fala_pb/audios/experimento_timbre/output/xtts_C1.wav"><a href="/fala_pb/audios/experimento_timbre/output/xtts_C1.wav">baixar audio</a></audio>
</div>
</div></div>
<div class="art-linha">
<p class="art-texto">A vida e feita de escolhas.</p>
<div class="art-cols">
<div class="art-col">
<span class="art-col-rot">Referencia de 10 s</span>
<audio controls preload="none" src="/fala_pb/audios/experimento_timbre/output/xtts_A2.wav"><a href="/fala_pb/audios/experimento_timbre/output/xtts_A2.wav">baixar audio</a></audio>
</div>
<div class="art-col">
<span class="art-col-rot">Referencia de 30 s</span>
<audio controls preload="none" src="/fala_pb/audios/experimento_timbre/output/xtts_B2.wav"><a href="/fala_pb/audios/experimento_timbre/output/xtts_B2.wav">baixar audio</a></audio>
</div>
<div class="art-col">
<span class="art-col-rot">Referencia de 60 s</span>
<audio controls preload="none" src="/fala_pb/audios/experimento_timbre/output/xtts_C2.wav"><a href="/fala_pb/audios/experimento_timbre/output/xtts_C2.wav">baixar audio</a></audio>
</div>
</div></div>
<div class="art-linha">
<p class="art-texto">Aprender nunca e demais.</p>
<div class="art-cols">
<div class="art-col">
<span class="art-col-rot">Referencia de 10 s</span>
<audio controls preload="none" src="/fala_pb/audios/experimento_timbre/output/xtts_A3.wav"><a href="/fala_pb/audios/experimento_timbre/output/xtts_A3.wav">baixar audio</a></audio>
</div>
<div class="art-col">
<span class="art-col-rot">Referencia de 30 s</span>
<audio controls preload="none" src="/fala_pb/audios/experimento_timbre/output/xtts_B3.wav"><a href="/fala_pb/audios/experimento_timbre/output/xtts_B3.wav">baixar audio</a></audio>
</div>
<div class="art-col">
<span class="art-col-rot">Referencia de 60 s</span>
<audio controls preload="none" src="/fala_pb/audios/experimento_timbre/output/xtts_C3.wav"><a href="/fala_pb/audios/experimento_timbre/output/xtts_C3.wav">baixar audio</a></audio>
</div>
</div></div>
<div class="art-linha">
<p class="art-texto">As bibliotecas publicas tem papel essencial na democratizacao do conhecimento, oferecendo nao so livros, mas tambem acesso a internet, cursos e espacos de convivencia para a comunidade local.</p>
<div class="art-cols">
<div class="art-col">
<span class="art-col-rot">Referencia de 10 s</span>
<audio controls preload="none" src="/fala_pb/audios/experimento_timbre/output/xtts_A4.wav"><a href="/fala_pb/audios/experimento_timbre/output/xtts_A4.wav">baixar audio</a></audio>
</div>
<div class="art-col">
<span class="art-col-rot">Referencia de 30 s</span>
<audio controls preload="none" src="/fala_pb/audios/experimento_timbre/output/xtts_B4.wav"><a href="/fala_pb/audios/experimento_timbre/output/xtts_B4.wav">baixar audio</a></audio>
</div>
<div class="art-col">
<span class="art-col-rot">Referencia de 60 s</span>
<audio controls preload="none" src="/fala_pb/audios/experimento_timbre/output/xtts_C4.wav"><a href="/fala_pb/audios/experimento_timbre/output/xtts_C4.wav">baixar audio</a></audio>
</div>
</div></div>
<div class="art-linha">
<p class="art-texto">Em um mundo cada vez mais conectado, e fundamental equilibrar o uso de dispositivos moveis com momentos de descanso e socializacao presencial, preservando nossa saude mental e bem-estar.</p>
<div class="art-cols">
<div class="art-col">
<span class="art-col-rot">Referencia de 10 s</span>
<audio controls preload="none" src="/fala_pb/audios/experimento_timbre/output/xtts_A5.wav"><a href="/fala_pb/audios/experimento_timbre/output/xtts_A5.wav">baixar audio</a></audio>
</div>
<div class="art-col">
<span class="art-col-rot">Referencia de 30 s</span>
<audio controls preload="none" src="/fala_pb/audios/experimento_timbre/output/xtts_B5.wav"><a href="/fala_pb/audios/experimento_timbre/output/xtts_B5.wav">baixar audio</a></audio>
</div>
<div class="art-col">
<span class="art-col-rot">Referencia de 60 s</span>
<audio controls preload="none" src="/fala_pb/audios/experimento_timbre/output/xtts_C5.wav"><a href="/fala_pb/audios/experimento_timbre/output/xtts_C5.wav">baixar audio</a></audio>
</div>
</div></div>
<div class="art-linha">
<p class="art-texto">Hoje o ceu amanheceu com nuvens carregadas e uma leve brisa.</p>
<div class="art-cols">
<div class="art-col">
<span class="art-col-rot">Referencia de 10 s</span>
<audio controls preload="none" src="/fala_pb/audios/experimento_timbre/output/xtts_A6.wav"><a href="/fala_pb/audios/experimento_timbre/output/xtts_A6.wav">baixar audio</a></audio>
</div>
<div class="art-col">
<span class="art-col-rot">Referencia de 30 s</span>
<audio controls preload="none" src="/fala_pb/audios/experimento_timbre/output/xtts_B6.wav"><a href="/fala_pb/audios/experimento_timbre/output/xtts_B6.wav">baixar audio</a></audio>
</div>
<div class="art-col">
<span class="art-col-rot">Referencia de 60 s</span>
<audio controls preload="none" src="/fala_pb/audios/experimento_timbre/output/xtts_C6.wav"><a href="/fala_pb/audios/experimento_timbre/output/xtts_C6.wav">baixar audio</a></audio>
</div>
</div></div>
<div class="art-linha">
<p class="art-texto">No interior da cidade, pracas antigas guardam historias de geracoes.</p>
<div class="art-cols">
<div class="art-col">
<span class="art-col-rot">Referencia de 10 s</span>
<audio controls preload="none" src="/fala_pb/audios/experimento_timbre/output/xtts_A7.wav"><a href="/fala_pb/audios/experimento_timbre/output/xtts_A7.wav">baixar audio</a></audio>
</div>
<div class="art-col">
<span class="art-col-rot">Referencia de 30 s</span>
<audio controls preload="none" src="/fala_pb/audios/experimento_timbre/output/xtts_B7.wav"><a href="/fala_pb/audios/experimento_timbre/output/xtts_B7.wav">baixar audio</a></audio>
</div>
<div class="art-col">
<span class="art-col-rot">Referencia de 60 s</span>
<audio controls preload="none" src="/fala_pb/audios/experimento_timbre/output/xtts_C7.wav"><a href="/fala_pb/audios/experimento_timbre/output/xtts_C7.wav">baixar audio</a></audio>
</div>
</div></div>
<div class="art-linha">
<p class="art-texto">O cafe fresco pela manha anima qualquer rotina.</p>
<div class="art-cols">
<div class="art-col">
<span class="art-col-rot">Referencia de 10 s</span>
<audio controls preload="none" src="/fala_pb/audios/experimento_timbre/output/xtts_A8.wav"><a href="/fala_pb/audios/experimento_timbre/output/xtts_A8.wav">baixar audio</a></audio>
</div>
<div class="art-col">
<span class="art-col-rot">Referencia de 30 s</span>
<audio controls preload="none" src="/fala_pb/audios/experimento_timbre/output/xtts_B8.wav"><a href="/fala_pb/audios/experimento_timbre/output/xtts_B8.wav">baixar audio</a></audio>
</div>
<div class="art-col">
<span class="art-col-rot">Referencia de 60 s</span>
<audio controls preload="none" src="/fala_pb/audios/experimento_timbre/output/xtts_C8.wav"><a href="/fala_pb/audios/experimento_timbre/output/xtts_C8.wav">baixar audio</a></audio>
</div>
</div></div>
<div class="art-linha">
<p class="art-texto">Ola, tudo bem?</p>
<div class="art-cols">
<div class="art-col">
<span class="art-col-rot">Referencia de 10 s</span>
<audio controls preload="none" src="/fala_pb/audios/experimento_timbre/output/xtts_A9.wav"><a href="/fala_pb/audios/experimento_timbre/output/xtts_A9.wav">baixar audio</a></audio>
</div>
<div class="art-col">
<span class="art-col-rot">Referencia de 30 s</span>
<audio controls preload="none" src="/fala_pb/audios/experimento_timbre/output/xtts_B9.wav"><a href="/fala_pb/audios/experimento_timbre/output/xtts_B9.wav">baixar audio</a></audio>
</div>
<div class="art-col">
<span class="art-col-rot">Referencia de 60 s</span>
<audio controls preload="none" src="/fala_pb/audios/experimento_timbre/output/xtts_C9.wav"><a href="/fala_pb/audios/experimento_timbre/output/xtts_C9.wav">baixar audio</a></audio>
</div>
</div></div>
<div class="art-linha">
<p class="art-texto">Projetos de ciencia cidada estimulam a participacao de voluntarios em coletas de dados ambientais e podem contribuir para pesquisas sobre mudancas climaticas, flora, fauna e qualidade da agua em diversas regioes.</p>
<div class="art-cols">
<div class="art-col">
<span class="art-col-rot">Referencia de 10 s</span>
<audio controls preload="none" src="/fala_pb/audios/experimento_timbre/output/xtts_A10.wav"><a href="/fala_pb/audios/experimento_timbre/output/xtts_A10.wav">baixar audio</a></audio>
</div>
<div class="art-col">
<span class="art-col-rot">Referencia de 30 s</span>
<audio controls preload="none" src="/fala_pb/audios/experimento_timbre/output/xtts_B10.wav"><a href="/fala_pb/audios/experimento_timbre/output/xtts_B10.wav">baixar audio</a></audio>
</div>
<div class="art-col">
<span class="art-col-rot">Referencia de 60 s</span>
<audio controls preload="none" src="/fala_pb/audios/experimento_timbre/output/xtts_C10.wav"><a href="/fala_pb/audios/experimento_timbre/output/xtts_C10.wav">baixar audio</a></audio>
</div>
</div></div>
</div>
</section>

<section class="art-bloco" id="xtts-ajuste-fino" markdown="0">
<h2>2. XTTS -- ajuste fino<span class="art-selo art-selo--pos">resultado positivo</span></h2>
<p class="art-topo">Estrategia: Ajuste fino &middot; <a href="#sumario">voltar ao sumario</a></p>
<div class="art-afirmacao"><strong>Afirmacao verificavel</strong>O ajuste fino incorporou o sotaque paraibano: tracos regionais passam a ser audiveis na saida do modelo, num sotaque misto em que convivem com o padrao do checkpoint base.</div>
<p class="art-desc">Mesma frase nas duas colunas, mesmo prompt de voz. A coluna <em>original</em> e o checkpoint publico do XTTS; a coluna <em>ajustado</em> e o melhor checkpoint do ajuste fino sobre o FALA_PB. Ouca sobretudo a realizacao das vogais atonas finais e o ritmo. Pagina completa: <a href="/fala_pb/15/">reuniao 15</a>.</p>
<div class="art-tabela">
<div class="art-linha">
<p class="art-texto">Hoje acordei cedo, preparei um café forte e organizei a mesa para estudar com calma.</p>
<div class="art-cols">
<div class="art-col">
<span class="art-col-rot">Referencia de voz</span>
<audio controls preload="none" src="/fala_pb/15/xtts/xtts_ref_frase01.wav"><a href="/fala_pb/15/xtts/xtts_ref_frase01.wav">baixar audio</a></audio>
</div>
<div class="art-col">
<span class="art-col-rot">Original (checkpoint base)</span>
<audio controls preload="none" src="/fala_pb/15/xtts/xtts_model_original_frase01.wav"><a href="/fala_pb/15/xtts/xtts_model_original_frase01.wav">baixar audio</a></audio>
</div>
<div class="art-col">
<span class="art-col-rot">Ajustado (FALA_PB)</span>
<audio controls preload="none" src="/fala_pb/15/xtts/xtts_model_best_frase01.wav"><a href="/fala_pb/15/xtts/xtts_model_best_frase01.wav">baixar audio</a></audio>
</div>
</div></div>
<div class="art-linha">
<p class="art-texto">Enquanto o trem passava devagar, uma criança sorria e apontava para as nuvens alaranjadas.</p>
<div class="art-cols">
<div class="art-col">
<span class="art-col-rot">Referencia de voz</span>
<audio controls preload="none" src="/fala_pb/15/xtts/xtts_ref_frase02.wav"><a href="/fala_pb/15/xtts/xtts_ref_frase02.wav">baixar audio</a></audio>
</div>
<div class="art-col">
<span class="art-col-rot">Original (checkpoint base)</span>
<audio controls preload="none" src="/fala_pb/15/xtts/xtts_model_original_frase02.wav"><a href="/fala_pb/15/xtts/xtts_model_original_frase02.wav">baixar audio</a></audio>
</div>
<div class="art-col">
<span class="art-col-rot">Ajustado (FALA_PB)</span>
<audio controls preload="none" src="/fala_pb/15/xtts/xtts_model_best_frase02.wav"><a href="/fala_pb/15/xtts/xtts_model_best_frase02.wav">baixar audio</a></audio>
</div>
</div></div>
<div class="art-linha">
<p class="art-texto">O pesquisador analisou os dados, escreveu um relatório objetivo e compartilhou as conclusões com a equipe.</p>
<div class="art-cols">
<div class="art-col">
<span class="art-col-rot">Referencia de voz</span>
<audio controls preload="none" src="/fala_pb/15/xtts/xtts_ref_frase03.wav"><a href="/fala_pb/15/xtts/xtts_ref_frase03.wav">baixar audio</a></audio>
</div>
<div class="art-col">
<span class="art-col-rot">Original (checkpoint base)</span>
<audio controls preload="none" src="/fala_pb/15/xtts/xtts_model_original_frase03.wav"><a href="/fala_pb/15/xtts/xtts_model_original_frase03.wav">baixar audio</a></audio>
</div>
<div class="art-col">
<span class="art-col-rot">Ajustado (FALA_PB)</span>
<audio controls preload="none" src="/fala_pb/15/xtts/xtts_model_best_frase03.wav"><a href="/fala_pb/15/xtts/xtts_model_best_frase03.wav">baixar audio</a></audio>
</div>
</div></div>
<div class="art-linha">
<p class="art-texto">Estamos construindo uma rotina mais saudável, caminhando no bairro e cozinhando alimentos frescos todos os dias.</p>
<div class="art-cols">
<div class="art-col">
<span class="art-col-rot">Referencia de voz</span>
<audio controls preload="none" src="/fala_pb/15/xtts/xtts_ref_frase04.wav"><a href="/fala_pb/15/xtts/xtts_ref_frase04.wav">baixar audio</a></audio>
</div>
<div class="art-col">
<span class="art-col-rot">Original (checkpoint base)</span>
<audio controls preload="none" src="/fala_pb/15/xtts/xtts_model_original_frase04.wav"><a href="/fala_pb/15/xtts/xtts_model_original_frase04.wav">baixar audio</a></audio>
</div>
<div class="art-col">
<span class="art-col-rot">Ajustado (FALA_PB)</span>
<audio controls preload="none" src="/fala_pb/15/xtts/xtts_model_best_frase04.wav"><a href="/fala_pb/15/xtts/xtts_model_best_frase04.wav">baixar audio</a></audio>
</div>
</div></div>
<div class="art-linha">
<p class="art-texto">A bibliotecária catalogou romances, dicionários e biografias, mantendo cada prateleira limpa e bem sinalizada.</p>
<div class="art-cols">
<div class="art-col">
<span class="art-col-rot">Referencia de voz</span>
<audio controls preload="none" src="/fala_pb/15/xtts/xtts_ref_frase05.wav"><a href="/fala_pb/15/xtts/xtts_ref_frase05.wav">baixar audio</a></audio>
</div>
<div class="art-col">
<span class="art-col-rot">Original (checkpoint base)</span>
<audio controls preload="none" src="/fala_pb/15/xtts/xtts_model_original_frase05.wav"><a href="/fala_pb/15/xtts/xtts_model_original_frase05.wav">baixar audio</a></audio>
</div>
<div class="art-col">
<span class="art-col-rot">Ajustado (FALA_PB)</span>
<audio controls preload="none" src="/fala_pb/15/xtts/xtts_model_best_frase05.wav"><a href="/fala_pb/15/xtts/xtts_model_best_frase05.wav">baixar audio</a></audio>
</div>
</div></div>
</div>
</section>

<section class="art-bloco" id="f5tts-ajuste-fino" markdown="0">
<h2>3. F5-TTS -- ajuste fino<span class="art-selo art-selo--neg">resultado negativo</span></h2>
<p class="art-topo">Estrategia: Ajuste fino &middot; <a href="#sumario">voltar ao sumario</a></p>
<div class="art-afirmacao"><strong>Afirmacao verificavel</strong>As saidas do modelo ajustado ficaram praticamente identicas as do checkpoint original, apesar de os pesos terem mudado ao longo do treino.</div>
<p class="art-desc">As duas colunas foram sintetizadas com a mesma semente e o mesmo prompt, variando apenas o checkpoint. A quase indistinguibilidade entre elas e o resultado -- e uma evidencia negativa, nao um erro de montagem da pagina. Pagina completa: <a href="/fala_pb/16/">reuniao 16</a>.</p>
<div class="art-tabela">
<div class="art-linha">
<p class="art-texto">Hoje acordei cedo, preparei um café forte e organizei a mesa para estudar com calma.</p>
<div class="art-cols">
<div class="art-col">
<span class="art-col-rot">Original (checkpoint base)</span>
<audio controls preload="none" src="/fala_pb/16/f5tts%20novo%20treino/filtered_checkpoint_original_line01.wav"><a href="/fala_pb/16/f5tts%20novo%20treino/filtered_checkpoint_original_line01.wav">baixar audio</a></audio>
</div>
<div class="art-col">
<span class="art-col-rot">Ajustado (FALA_PB, ultimo checkpoint)</span>
<audio controls preload="none" src="/fala_pb/16/f5tts%20novo%20treino/filtered_model_last_line01.wav"><a href="/fala_pb/16/f5tts%20novo%20treino/filtered_model_last_line01.wav">baixar audio</a></audio>
</div>
</div></div>
<div class="art-linha">
<p class="art-texto">Enquanto o trem passava devagar, uma criança sorria e apontava para as nuvens alaranjadas.</p>
<div class="art-cols">
<div class="art-col">
<span class="art-col-rot">Original (checkpoint base)</span>
<audio controls preload="none" src="/fala_pb/16/f5tts%20novo%20treino/filtered_checkpoint_original_line02.wav"><a href="/fala_pb/16/f5tts%20novo%20treino/filtered_checkpoint_original_line02.wav">baixar audio</a></audio>
</div>
<div class="art-col">
<span class="art-col-rot">Ajustado (FALA_PB, ultimo checkpoint)</span>
<audio controls preload="none" src="/fala_pb/16/f5tts%20novo%20treino/filtered_model_last_line02.wav"><a href="/fala_pb/16/f5tts%20novo%20treino/filtered_model_last_line02.wav">baixar audio</a></audio>
</div>
</div></div>
<div class="art-linha">
<p class="art-texto">O pesquisador analisou os dados, escreveu um relatório objetivo e compartilhou as conclusões com a equipe.</p>
<div class="art-cols">
<div class="art-col">
<span class="art-col-rot">Original (checkpoint base)</span>
<audio controls preload="none" src="/fala_pb/16/f5tts%20novo%20treino/filtered_checkpoint_original_line03.wav"><a href="/fala_pb/16/f5tts%20novo%20treino/filtered_checkpoint_original_line03.wav">baixar audio</a></audio>
</div>
<div class="art-col">
<span class="art-col-rot">Ajustado (FALA_PB, ultimo checkpoint)</span>
<audio controls preload="none" src="/fala_pb/16/f5tts%20novo%20treino/filtered_model_last_line03.wav"><a href="/fala_pb/16/f5tts%20novo%20treino/filtered_model_last_line03.wav">baixar audio</a></audio>
</div>
</div></div>
<div class="art-linha">
<p class="art-texto">Estamos construindo uma rotina mais saudável, caminhando no bairro e cozinhando alimentos frescos todos os dias.</p>
<div class="art-cols">
<div class="art-col">
<span class="art-col-rot">Original (checkpoint base)</span>
<audio controls preload="none" src="/fala_pb/16/f5tts%20novo%20treino/filtered_checkpoint_original_line04.wav"><a href="/fala_pb/16/f5tts%20novo%20treino/filtered_checkpoint_original_line04.wav">baixar audio</a></audio>
</div>
<div class="art-col">
<span class="art-col-rot">Ajustado (FALA_PB, ultimo checkpoint)</span>
<audio controls preload="none" src="/fala_pb/16/f5tts%20novo%20treino/filtered_model_last_line04.wav"><a href="/fala_pb/16/f5tts%20novo%20treino/filtered_model_last_line04.wav">baixar audio</a></audio>
</div>
</div></div>
<div class="art-linha">
<p class="art-texto">A bibliotecária catalogou romances, dicionários e biografias, mantendo cada prateleira limpa e bem sinalizada.</p>
<div class="art-cols">
<div class="art-col">
<span class="art-col-rot">Original (checkpoint base)</span>
<audio controls preload="none" src="/fala_pb/16/f5tts%20novo%20treino/filtered_checkpoint_original_line05.wav"><a href="/fala_pb/16/f5tts%20novo%20treino/filtered_checkpoint_original_line05.wav">baixar audio</a></audio>
</div>
<div class="art-col">
<span class="art-col-rot">Ajustado (FALA_PB, ultimo checkpoint)</span>
<audio controls preload="none" src="/fala_pb/16/f5tts%20novo%20treino/filtered_model_last_line05.wav"><a href="/fala_pb/16/f5tts%20novo%20treino/filtered_model_last_line05.wav">baixar audio</a></audio>
</div>
</div></div>
</div>
</section>

<section class="art-bloco" id="orpheus-ajuste-fino" markdown="0">
<h2>4. Orpheus TTS -- ajuste fino<span class="art-selo art-selo--pos">resultado positivo</span></h2>
<p class="art-topo">Estrategia: Ajuste fino &middot; <a href="#sumario">voltar ao sumario</a></p>
<div class="art-afirmacao"><strong>Afirmacao verificavel</strong>A incorporacao do sotaque paraibano foi satisfatoria.</div>
<p class="art-desc">Este e o bloco em que a adaptacao mais se ouve. Compare a coluna <em>ajustado</em> com a <em>original</em>: a diferenca esperada esta na abertura das vogais pretonicas e no contorno entoacional. Paginas completas: <a href="/fala_pb/15/">reuniao 15</a> e <a href="/fala_pb/16/">reuniao 16</a>.</p>
<div class="art-tabela">
<h3>Cinco frases fixas de acompanhamento</h3>
<p class="art-nota">Para o Orpheus nao foi preservada a sintese do checkpoint base sobre estas cinco frases; a comparacao original x ajustado aparece na tabela seguinte, sobre as sentencas da avaliacao final.</p>
<div class="art-linha">
<p class="art-texto">Hoje acordei cedo, preparei um café forte e organizei a mesa para estudar com calma.</p>
<div class="art-cols">
<div class="art-col">
<span class="art-col-rot">Ajustado (FALA_PB, 1 epoca)</span>
<audio controls preload="none" src="/fala_pb/15/artoodtoo_ft_e3/audios%20experimento/unsloth_artoodtoo_model_1_frase01.wav"><a href="/fala_pb/15/artoodtoo_ft_e3/audios%20experimento/unsloth_artoodtoo_model_1_frase01.wav">baixar audio</a></audio>
</div>
</div></div>
<div class="art-linha">
<p class="art-texto">Enquanto o trem passava devagar, uma criança sorria e apontava para as nuvens alaranjadas.</p>
<div class="art-cols">
<div class="art-col">
<span class="art-col-rot">Ajustado (FALA_PB, 1 epoca)</span>
<audio controls preload="none" src="/fala_pb/15/artoodtoo_ft_e3/audios%20experimento/unsloth_artoodtoo_model_1_frase02.wav"><a href="/fala_pb/15/artoodtoo_ft_e3/audios%20experimento/unsloth_artoodtoo_model_1_frase02.wav">baixar audio</a></audio>
</div>
</div></div>
<div class="art-linha">
<p class="art-texto">O pesquisador analisou os dados, escreveu um relatório objetivo e compartilhou as conclusões com a equipe.</p>
<div class="art-cols">
<div class="art-col">
<span class="art-col-rot">Ajustado (FALA_PB, 1 epoca)</span>
<audio controls preload="none" src="/fala_pb/15/artoodtoo_ft_e3/audios%20experimento/unsloth_artoodtoo_model_1_frase03.wav"><a href="/fala_pb/15/artoodtoo_ft_e3/audios%20experimento/unsloth_artoodtoo_model_1_frase03.wav">baixar audio</a></audio>
</div>
</div></div>
<div class="art-linha">
<p class="art-texto">Estamos construindo uma rotina mais saudável, caminhando no bairro e cozinhando alimentos frescos todos os dias.</p>
<div class="art-cols">
<div class="art-col">
<span class="art-col-rot">Ajustado (FALA_PB, 1 epoca)</span>
<audio controls preload="none" src="/fala_pb/15/artoodtoo_ft_e3/audios%20experimento/unsloth_artoodtoo_model_1_frase04.wav"><a href="/fala_pb/15/artoodtoo_ft_e3/audios%20experimento/unsloth_artoodtoo_model_1_frase04.wav">baixar audio</a></audio>
</div>
</div></div>
<div class="art-linha">
<p class="art-texto">A bibliotecária catalogou romances, dicionários e biografias, mantendo cada prateleira limpa e bem sinalizada.</p>
<div class="art-cols">
<div class="art-col">
<span class="art-col-rot">Ajustado (FALA_PB, 1 epoca)</span>
<audio controls preload="none" src="/fala_pb/15/artoodtoo_ft_e3/audios%20experimento/unsloth_artoodtoo_model_1_frase05.wav"><a href="/fala_pb/15/artoodtoo_ft_e3/audios%20experimento/unsloth_artoodtoo_model_1_frase05.wav">baixar audio</a></audio>
</div>
</div></div>
</div>
<div class="art-tabela">
<h3>Original x ajustado (sentencas da avaliacao final)</h3>
<p class="art-nota">Cinco sentencas do conjunto de 100, na versao eleita pelo criterio melhor-de-3. Mesma sentenca nas duas colunas.</p>
<div class="art-linha">
<p class="art-rotulo-linha">Sentenca 001</p>
<p class="art-texto">Hoje o trânsito estava tranquilo.</p>
<div class="art-cols">
<div class="art-col">
<span class="art-col-rot">Original (checkpoint base)</span>
<audio controls preload="none" src="/fala_pb/Inferencias%20finais/Audios/unsloth/outputs_final_experiment/original/v3/001.wav"><a href="/fala_pb/Inferencias%20finais/Audios/unsloth/outputs_final_experiment/original/v3/001.wav">baixar audio</a></audio>
</div>
<div class="art-col">
<span class="art-col-rot">Ajustado (FALA_PB)</span>
<audio controls preload="none" src="/fala_pb/Inferencias%20finais/Audios/unsloth/outputs_final_experiment/ajustado/v2/001.wav"><a href="/fala_pb/Inferencias%20finais/Audios/unsloth/outputs_final_experiment/ajustado/v2/001.wav">baixar audio</a></audio>
</div>
</div></div>
<div class="art-linha">
<p class="art-rotulo-linha">Sentenca 003</p>
<p class="art-texto">Depois de muito procurar, finalmente encontrei as chaves que havia perdido durante a mudança.</p>
<div class="art-cols">
<div class="art-col">
<span class="art-col-rot">Original (checkpoint base)</span>
<audio controls preload="none" src="/fala_pb/Inferencias%20finais/Audios/unsloth/outputs_final_experiment/original/v2/003.wav"><a href="/fala_pb/Inferencias%20finais/Audios/unsloth/outputs_final_experiment/original/v2/003.wav">baixar audio</a></audio>
</div>
<div class="art-col">
<span class="art-col-rot">Ajustado (FALA_PB)</span>
<audio controls preload="none" src="/fala_pb/Inferencias%20finais/Audios/unsloth/outputs_final_experiment/ajustado/v2/003.wav"><a href="/fala_pb/Inferencias%20finais/Audios/unsloth/outputs_final_experiment/ajustado/v2/003.wav">baixar audio</a></audio>
</div>
</div></div>
<div class="art-linha">
<p class="art-rotulo-linha">Sentenca 012</p>
<p class="art-texto">Quando chegamos ao local do evento, a apresentação já havia começado e quase não encontramos lugares disponíveis.</p>
<div class="art-cols">
<div class="art-col">
<span class="art-col-rot">Original (checkpoint base)</span>
<audio controls preload="none" src="/fala_pb/Inferencias%20finais/Audios/unsloth/outputs_final_experiment/original/v2/012.wav"><a href="/fala_pb/Inferencias%20finais/Audios/unsloth/outputs_final_experiment/original/v2/012.wav">baixar audio</a></audio>
</div>
<div class="art-col">
<span class="art-col-rot">Ajustado (FALA_PB)</span>
<audio controls preload="none" src="/fala_pb/Inferencias%20finais/Audios/unsloth/outputs_final_experiment/ajustado/v1/012.wav"><a href="/fala_pb/Inferencias%20finais/Audios/unsloth/outputs_final_experiment/ajustado/v1/012.wav">baixar audio</a></audio>
</div>
</div></div>
<div class="art-linha">
<p class="art-rotulo-linha">Sentenca 036</p>
<p class="art-texto">A praia estava praticamente vazia naquela manhã de terça-feira.</p>
<div class="art-cols">
<div class="art-col">
<span class="art-col-rot">Original (checkpoint base)</span>
<audio controls preload="none" src="/fala_pb/Inferencias%20finais/Audios/unsloth/outputs_final_experiment/original/v2/036.wav"><a href="/fala_pb/Inferencias%20finais/Audios/unsloth/outputs_final_experiment/original/v2/036.wav">baixar audio</a></audio>
</div>
<div class="art-col">
<span class="art-col-rot">Ajustado (FALA_PB)</span>
<audio controls preload="none" src="/fala_pb/Inferencias%20finais/Audios/unsloth/outputs_final_experiment/ajustado/v1/036.wav"><a href="/fala_pb/Inferencias%20finais/Audios/unsloth/outputs_final_experiment/ajustado/v1/036.wav">baixar audio</a></audio>
</div>
</div></div>
<div class="art-linha">
<p class="art-rotulo-linha">Sentenca 071</p>
<p class="art-texto">O médico chegou pontualmente.</p>
<div class="art-cols">
<div class="art-col">
<span class="art-col-rot">Original (checkpoint base)</span>
<audio controls preload="none" src="/fala_pb/Inferencias%20finais/Audios/unsloth/outputs_final_experiment/original/v1/071.wav"><a href="/fala_pb/Inferencias%20finais/Audios/unsloth/outputs_final_experiment/original/v1/071.wav">baixar audio</a></audio>
</div>
<div class="art-col">
<span class="art-col-rot">Ajustado (FALA_PB)</span>
<audio controls preload="none" src="/fala_pb/Inferencias%20finais/Audios/unsloth/outputs_final_experiment/ajustado/v2/071.wav"><a href="/fala_pb/Inferencias%20finais/Audios/unsloth/outputs_final_experiment/ajustado/v2/071.wav">baixar audio</a></audio>
</div>
</div></div>
</div>
</section>

<section class="art-bloco" id="fishspeech-ajuste-fino" markdown="0">
<h2>5. Fish Speech -- ajuste fino<span class="art-selo art-selo--pos">resultado positivo</span></h2>
<p class="art-topo">Estrategia: Ajuste fino &middot; <a href="#sumario">voltar ao sumario</a></p>
<div class="art-afirmacao"><strong>Afirmacao verificavel</strong>Uma unica epoca de ajuste fino (LoRA) ja bastou para tornar o sotaque paraibano perceptivel nas sinteses.</div>
<p class="art-desc">Mesmo prompt de voz de referencia nas duas colunas. Compare a coluna <em>ajustado</em> com a <em>original</em>: a adaptacao se ouve com mais forca em algumas frases do que em outras, o que era de esperar de um treino de uma unica epoca. Ouca as cinco. Pagina completa: <a href="/fala_pb/17/">reuniao 17</a>.</p>
<div class="art-tabela">
<div class="art-linha">
<p class="art-texto">Hoje acordei cedo, preparei um café forte e organizei a mesa para estudar com calma.</p>
<div class="art-cols">
<div class="art-col">
<span class="art-col-rot">Prompt de referencia</span>
<audio controls preload="none" src="/fala_pb/17/fishspeech/reference_prompt.wav"><a href="/fala_pb/17/fishspeech/reference_prompt.wav">baixar audio</a></audio>
</div>
<div class="art-col">
<span class="art-col-rot">Original (Fish Speech 1.5)</span>
<audio controls preload="none" src="/fala_pb/17/fishspeech/baseline_phrase_01.wav"><a href="/fala_pb/17/fishspeech/baseline_phrase_01.wav">baixar audio</a></audio>
</div>
<div class="art-col">
<span class="art-col-rot">Ajustado (LoRA, 1 epoca)</span>
<audio controls preload="none" src="/fala_pb/17/fishspeech/step_000010488_phrase_01.wav"><a href="/fala_pb/17/fishspeech/step_000010488_phrase_01.wav">baixar audio</a></audio>
</div>
</div></div>
<div class="art-linha">
<p class="art-texto">Enquanto o trem passava devagar, uma criança sorria e apontava para as nuvens alaranjadas.</p>
<div class="art-cols">
<div class="art-col">
<span class="art-col-rot">Prompt de referencia</span>
<audio controls preload="none" src="/fala_pb/17/fishspeech/reference_prompt.wav"><a href="/fala_pb/17/fishspeech/reference_prompt.wav">baixar audio</a></audio>
</div>
<div class="art-col">
<span class="art-col-rot">Original (Fish Speech 1.5)</span>
<audio controls preload="none" src="/fala_pb/17/fishspeech/baseline_phrase_02.wav"><a href="/fala_pb/17/fishspeech/baseline_phrase_02.wav">baixar audio</a></audio>
</div>
<div class="art-col">
<span class="art-col-rot">Ajustado (LoRA, 1 epoca)</span>
<audio controls preload="none" src="/fala_pb/17/fishspeech/step_000010488_phrase_02.wav"><a href="/fala_pb/17/fishspeech/step_000010488_phrase_02.wav">baixar audio</a></audio>
</div>
</div></div>
<div class="art-linha">
<p class="art-texto">O pesquisador analisou os dados, escreveu um relatório objetivo e compartilhou as conclusões com a equipe.</p>
<div class="art-cols">
<div class="art-col">
<span class="art-col-rot">Prompt de referencia</span>
<audio controls preload="none" src="/fala_pb/17/fishspeech/reference_prompt.wav"><a href="/fala_pb/17/fishspeech/reference_prompt.wav">baixar audio</a></audio>
</div>
<div class="art-col">
<span class="art-col-rot">Original (Fish Speech 1.5)</span>
<audio controls preload="none" src="/fala_pb/17/fishspeech/baseline_phrase_03.wav"><a href="/fala_pb/17/fishspeech/baseline_phrase_03.wav">baixar audio</a></audio>
</div>
<div class="art-col">
<span class="art-col-rot">Ajustado (LoRA, 1 epoca)</span>
<audio controls preload="none" src="/fala_pb/17/fishspeech/step_000010488_phrase_03.wav"><a href="/fala_pb/17/fishspeech/step_000010488_phrase_03.wav">baixar audio</a></audio>
</div>
</div></div>
<div class="art-linha">
<p class="art-texto">Estamos construindo uma rotina mais saudável, caminhando no bairro e cozinhando alimentos frescos todos os dias.</p>
<div class="art-cols">
<div class="art-col">
<span class="art-col-rot">Prompt de referencia</span>
<audio controls preload="none" src="/fala_pb/17/fishspeech/reference_prompt.wav"><a href="/fala_pb/17/fishspeech/reference_prompt.wav">baixar audio</a></audio>
</div>
<div class="art-col">
<span class="art-col-rot">Original (Fish Speech 1.5)</span>
<audio controls preload="none" src="/fala_pb/17/fishspeech/baseline_phrase_04.wav"><a href="/fala_pb/17/fishspeech/baseline_phrase_04.wav">baixar audio</a></audio>
</div>
<div class="art-col">
<span class="art-col-rot">Ajustado (LoRA, 1 epoca)</span>
<audio controls preload="none" src="/fala_pb/17/fishspeech/step_000010488_phrase_04.wav"><a href="/fala_pb/17/fishspeech/step_000010488_phrase_04.wav">baixar audio</a></audio>
</div>
</div></div>
<div class="art-linha">
<p class="art-texto">A bibliotecária catalogou romances, dicionários e biografias, mantendo cada prateleira limpa e bem sinalizada.</p>
<div class="art-cols">
<div class="art-col">
<span class="art-col-rot">Prompt de referencia</span>
<audio controls preload="none" src="/fala_pb/17/fishspeech/reference_prompt.wav"><a href="/fala_pb/17/fishspeech/reference_prompt.wav">baixar audio</a></audio>
</div>
<div class="art-col">
<span class="art-col-rot">Original (Fish Speech 1.5)</span>
<audio controls preload="none" src="/fala_pb/17/fishspeech/baseline_phrase_05.wav"><a href="/fala_pb/17/fishspeech/baseline_phrase_05.wav">baixar audio</a></audio>
</div>
<div class="art-col">
<span class="art-col-rot">Ajustado (LoRA, 1 epoca)</span>
<audio controls preload="none" src="/fala_pb/17/fishspeech/step_000010488_phrase_05.wav"><a href="/fala_pb/17/fishspeech/step_000010488_phrase_05.wav">baixar audio</a></audio>
</div>
</div></div>
</div>
</section>

<section class="art-bloco" id="qwen3-ajuste-fino" markdown="0">
<h2>6. Qwen3-TTS -- ajuste fino<span class="art-selo art-selo--neg">resultado negativo</span></h2>
<p class="art-topo">Estrategia: Ajuste fino &middot; <a href="#sumario">voltar ao sumario</a></p>
<div class="art-afirmacao"><strong>Afirmacao verificavel</strong>A perda de treino caiu ao longo dos checkpoints, mas nao houve aproximacao audivel ao sotaque paraibano.</div>
<p class="art-desc">Tres checkpoints intermediarios (5 mil, 10 mil e 15 mil passos) comparados ao baseline anterior ao ajuste. O que se espera ouvir e ausencia de progressao: as quatro colunas soam equivalentes quanto ao sotaque. Pagina completa: <a href="/fala_pb/18/">reuniao 18</a>.</p>
<div class="art-tabela">
<div class="art-linha">
<p class="art-texto">Hoje acordei cedo, preparei um café forte e organizei a mesa para estudar com calma.</p>
<div class="art-cols">
<div class="art-col">
<span class="art-col-rot">Original (baseline)</span>
<audio controls preload="none" src="/fala_pb/18/QWEEN%20-%20TTS/outputs/pre_finetune_baseline_case_01.wav"><a href="/fala_pb/18/QWEEN%20-%20TTS/outputs/pre_finetune_baseline_case_01.wav">baixar audio</a></audio>
</div>
<div class="art-col">
<span class="art-col-rot">Ajustado - 5.000 passos</span>
<audio controls preload="none" src="/fala_pb/18/QWEEN%20-%20TTS/outputs/step_5000_frase1.wav"><a href="/fala_pb/18/QWEEN%20-%20TTS/outputs/step_5000_frase1.wav">baixar audio</a></audio>
</div>
<div class="art-col">
<span class="art-col-rot">Ajustado - 10.000 passos</span>
<audio controls preload="none" src="/fala_pb/18/QWEEN%20-%20TTS/outputs/step_10000_frase1.wav"><a href="/fala_pb/18/QWEEN%20-%20TTS/outputs/step_10000_frase1.wav">baixar audio</a></audio>
</div>
<div class="art-col">
<span class="art-col-rot">Ajustado - 15.000 passos</span>
<audio controls preload="none" src="/fala_pb/18/QWEEN%20-%20TTS/outputs/step_15000_frase1.wav"><a href="/fala_pb/18/QWEEN%20-%20TTS/outputs/step_15000_frase1.wav">baixar audio</a></audio>
</div>
</div></div>
<div class="art-linha">
<p class="art-texto">Enquanto o trem passava devagar, uma criança sorria e apontava para as nuvens alaranjadas.</p>
<div class="art-cols">
<div class="art-col">
<span class="art-col-rot">Original (baseline)</span>
<audio controls preload="none" src="/fala_pb/18/QWEEN%20-%20TTS/outputs/pre_finetune_baseline_case_02.wav"><a href="/fala_pb/18/QWEEN%20-%20TTS/outputs/pre_finetune_baseline_case_02.wav">baixar audio</a></audio>
</div>
<div class="art-col">
<span class="art-col-rot">Ajustado - 5.000 passos</span>
<audio controls preload="none" src="/fala_pb/18/QWEEN%20-%20TTS/outputs/step_5000_frase2.wav"><a href="/fala_pb/18/QWEEN%20-%20TTS/outputs/step_5000_frase2.wav">baixar audio</a></audio>
</div>
<div class="art-col">
<span class="art-col-rot">Ajustado - 10.000 passos</span>
<audio controls preload="none" src="/fala_pb/18/QWEEN%20-%20TTS/outputs/step_10000_frase2.wav"><a href="/fala_pb/18/QWEEN%20-%20TTS/outputs/step_10000_frase2.wav">baixar audio</a></audio>
</div>
<div class="art-col">
<span class="art-col-rot">Ajustado - 15.000 passos</span>
<audio controls preload="none" src="/fala_pb/18/QWEEN%20-%20TTS/outputs/step_15000_frase2.wav"><a href="/fala_pb/18/QWEEN%20-%20TTS/outputs/step_15000_frase2.wav">baixar audio</a></audio>
</div>
</div></div>
<div class="art-linha">
<p class="art-texto">O pesquisador analisou os dados, escreveu um relatório objetivo e compartilhou as conclusões com a equipe.</p>
<div class="art-cols">
<div class="art-col">
<span class="art-col-rot">Original (baseline)</span>
<audio controls preload="none" src="/fala_pb/18/QWEEN%20-%20TTS/outputs/pre_finetune_baseline_case_03.wav"><a href="/fala_pb/18/QWEEN%20-%20TTS/outputs/pre_finetune_baseline_case_03.wav">baixar audio</a></audio>
</div>
<div class="art-col">
<span class="art-col-rot">Ajustado - 5.000 passos</span>
<audio controls preload="none" src="/fala_pb/18/QWEEN%20-%20TTS/outputs/step_5000_frase3.wav"><a href="/fala_pb/18/QWEEN%20-%20TTS/outputs/step_5000_frase3.wav">baixar audio</a></audio>
</div>
<div class="art-col">
<span class="art-col-rot">Ajustado - 10.000 passos</span>
<audio controls preload="none" src="/fala_pb/18/QWEEN%20-%20TTS/outputs/step_10000_frase3.wav"><a href="/fala_pb/18/QWEEN%20-%20TTS/outputs/step_10000_frase3.wav">baixar audio</a></audio>
</div>
<div class="art-col">
<span class="art-col-rot">Ajustado - 15.000 passos</span>
<audio controls preload="none" src="/fala_pb/18/QWEEN%20-%20TTS/outputs/step_15000_frase3.wav"><a href="/fala_pb/18/QWEEN%20-%20TTS/outputs/step_15000_frase3.wav">baixar audio</a></audio>
</div>
</div></div>
<div class="art-linha">
<p class="art-texto">Estamos construindo uma rotina mais saudável, caminhando no bairro e cozinhando alimentos frescos todos os dias.</p>
<div class="art-cols">
<div class="art-col">
<span class="art-col-rot">Original (baseline)</span>
<audio controls preload="none" src="/fala_pb/18/QWEEN%20-%20TTS/outputs/pre_finetune_baseline_case_04.wav"><a href="/fala_pb/18/QWEEN%20-%20TTS/outputs/pre_finetune_baseline_case_04.wav">baixar audio</a></audio>
</div>
<div class="art-col">
<span class="art-col-rot">Ajustado - 5.000 passos</span>
<audio controls preload="none" src="/fala_pb/18/QWEEN%20-%20TTS/outputs/step_5000_frase4.wav"><a href="/fala_pb/18/QWEEN%20-%20TTS/outputs/step_5000_frase4.wav">baixar audio</a></audio>
</div>
<div class="art-col">
<span class="art-col-rot">Ajustado - 10.000 passos</span>
<audio controls preload="none" src="/fala_pb/18/QWEEN%20-%20TTS/outputs/step_10000_frase4.wav"><a href="/fala_pb/18/QWEEN%20-%20TTS/outputs/step_10000_frase4.wav">baixar audio</a></audio>
</div>
<div class="art-col">
<span class="art-col-rot">Ajustado - 15.000 passos</span>
<audio controls preload="none" src="/fala_pb/18/QWEEN%20-%20TTS/outputs/step_15000_frase4.wav"><a href="/fala_pb/18/QWEEN%20-%20TTS/outputs/step_15000_frase4.wav">baixar audio</a></audio>
</div>
</div></div>
<div class="art-linha">
<p class="art-texto">A bibliotecária catalogou romances, dicionários e biografias, mantendo cada prateleira limpa e bem sinalizada.</p>
<div class="art-cols">
<div class="art-col">
<span class="art-col-rot">Original (baseline)</span>
<audio controls preload="none" src="/fala_pb/18/QWEEN%20-%20TTS/outputs/pre_finetune_baseline_case_05.wav"><a href="/fala_pb/18/QWEEN%20-%20TTS/outputs/pre_finetune_baseline_case_05.wav">baixar audio</a></audio>
</div>
<div class="art-col">
<span class="art-col-rot">Ajustado - 5.000 passos</span>
<audio controls preload="none" src="/fala_pb/18/QWEEN%20-%20TTS/outputs/step_5000_frase5.wav"><a href="/fala_pb/18/QWEEN%20-%20TTS/outputs/step_5000_frase5.wav">baixar audio</a></audio>
</div>
<div class="art-col">
<span class="art-col-rot">Ajustado - 10.000 passos</span>
<audio controls preload="none" src="/fala_pb/18/QWEEN%20-%20TTS/outputs/step_10000_frase5.wav"><a href="/fala_pb/18/QWEEN%20-%20TTS/outputs/step_10000_frase5.wav">baixar audio</a></audio>
</div>
<div class="art-col">
<span class="art-col-rot">Ajustado - 15.000 passos</span>
<audio controls preload="none" src="/fala_pb/18/QWEEN%20-%20TTS/outputs/step_15000_frase5.wav"><a href="/fala_pb/18/QWEEN%20-%20TTS/outputs/step_15000_frase5.wav">baixar audio</a></audio>
</div>
</div></div>
</div>
</section>

<section class="art-bloco" id="f5tts-do-zero" markdown="0">
<h2>7. F5-TTS treinado a partir de pesos aleatorios<span class="art-selo art-selo--neg">resultado negativo</span></h2>
<p class="art-topo">Estrategia: Treinamento a partir de pesos aleatorios &middot; <a href="#sumario">voltar ao sumario</a></p>
<div class="art-afirmacao"><strong>Afirmacao verificavel</strong>O checkpoint final (epoca 150) produz saidas ininteligiveis: as 111 h do FALA_PB nao bastam para treinar o modelo do zero.</div>
<p class="art-desc">Evidencia negativa. Nao ha coluna <em>original</em> aqui porque nao existe checkpoint base -- o treino partiu de pesos aleatorios. A referencia de voz esta na primeira coluna para dar a medida do que se esperava obter. Pagina completa: <a href="/fala_pb/19/">reuniao 19</a>.</p>
<div class="art-tabela">
<div class="art-linha">
<p class="art-texto">Hoje acordei cedo, preparei um café forte e organizei a mesa para estudar com calma.</p>
<div class="art-cols">
<div class="art-col">
<span class="art-col-rot">Referencia de voz</span>
<audio controls preload="none" src="/fala_pb/19/f5tts_do_zero/PB_0991_ref.wav"><a href="/fala_pb/19/f5tts_do_zero/PB_0991_ref.wav">baixar audio</a></audio>
</div>
<div class="art-col">
<span class="art-col-rot">Do zero (epoca 150, checkpoint final)</span>
<audio controls preload="none" src="/fala_pb/19/f5tts_do_zero/zero_model_last_line01.wav"><a href="/fala_pb/19/f5tts_do_zero/zero_model_last_line01.wav">baixar audio</a></audio>
</div>
</div></div>
<div class="art-linha">
<p class="art-texto">Enquanto o trem passava devagar, uma criança sorria e apontava para as nuvens alaranjadas.</p>
<div class="art-cols">
<div class="art-col">
<span class="art-col-rot">Referencia de voz</span>
<audio controls preload="none" src="/fala_pb/19/f5tts_do_zero/PB_0991_ref.wav"><a href="/fala_pb/19/f5tts_do_zero/PB_0991_ref.wav">baixar audio</a></audio>
</div>
<div class="art-col">
<span class="art-col-rot">Do zero (epoca 150, checkpoint final)</span>
<audio controls preload="none" src="/fala_pb/19/f5tts_do_zero/zero_model_last_line02.wav"><a href="/fala_pb/19/f5tts_do_zero/zero_model_last_line02.wav">baixar audio</a></audio>
</div>
</div></div>
<div class="art-linha">
<p class="art-texto">O pesquisador analisou os dados, escreveu um relatório objetivo e compartilhou as conclusões com a equipe.</p>
<div class="art-cols">
<div class="art-col">
<span class="art-col-rot">Referencia de voz</span>
<audio controls preload="none" src="/fala_pb/19/f5tts_do_zero/PB_0991_ref.wav"><a href="/fala_pb/19/f5tts_do_zero/PB_0991_ref.wav">baixar audio</a></audio>
</div>
<div class="art-col">
<span class="art-col-rot">Do zero (epoca 150, checkpoint final)</span>
<audio controls preload="none" src="/fala_pb/19/f5tts_do_zero/zero_model_last_line03.wav"><a href="/fala_pb/19/f5tts_do_zero/zero_model_last_line03.wav">baixar audio</a></audio>
</div>
</div></div>
<div class="art-linha">
<p class="art-texto">Estamos construindo uma rotina mais saudável, caminhando no bairro e cozinhando alimentos frescos todos os dias.</p>
<div class="art-cols">
<div class="art-col">
<span class="art-col-rot">Referencia de voz</span>
<audio controls preload="none" src="/fala_pb/19/f5tts_do_zero/PB_0991_ref.wav"><a href="/fala_pb/19/f5tts_do_zero/PB_0991_ref.wav">baixar audio</a></audio>
</div>
<div class="art-col">
<span class="art-col-rot">Do zero (epoca 150, checkpoint final)</span>
<audio controls preload="none" src="/fala_pb/19/f5tts_do_zero/zero_model_last_line04.wav"><a href="/fala_pb/19/f5tts_do_zero/zero_model_last_line04.wav">baixar audio</a></audio>
</div>
</div></div>
<div class="art-linha">
<p class="art-texto">A bibliotecária catalogou romances, dicionários e biografias, mantendo cada prateleira limpa e bem sinalizada.</p>
<div class="art-cols">
<div class="art-col">
<span class="art-col-rot">Referencia de voz</span>
<audio controls preload="none" src="/fala_pb/19/f5tts_do_zero/PB_0991_ref.wav"><a href="/fala_pb/19/f5tts_do_zero/PB_0991_ref.wav">baixar audio</a></audio>
</div>
<div class="art-col">
<span class="art-col-rot">Do zero (epoca 150, checkpoint final)</span>
<audio controls preload="none" src="/fala_pb/19/f5tts_do_zero/zero_model_last_line05.wav"><a href="/fala_pb/19/f5tts_do_zero/zero_model_last_line05.wav">baixar audio</a></audio>
</div>
</div></div>
</div>
</section>

<section class="art-bloco" id="avaliacao-automatica" markdown="0">
<h2>8. Avaliacao automatica -- conjunto completo<span class="art-selo art-selo--ref">conjunto de referencia</span></h2>
<p class="art-topo">Estrategia: Ajuste fino (tres modelos) &middot; <a href="#sumario">voltar ao sumario</a></p>
<div class="art-afirmacao"><strong>Afirmacao verificavel</strong>As metricas objetivas reportadas na dissertacao foram calculadas sobre 600 audios: 3 modelos x 2 condicoes x 100 sentencas, cada um eleito por melhor-de-3 entre tres sinteses independentes (1.800 sinteses no total).</div>
<p class="art-desc">Este conjunto nao e listado item a item aqui. Abaixo estao cinco sentencas por modelo, na versao efetivamente usada nas metricas, como amostra. O catalogo completo dos 1.800 audios, com filtros por modelo e condicao, esta na <strong><a href="/fala_pb/100/">pagina de inferencias finais</a></strong>.</p>
<div class="art-tabela">
<h3>XTTS</h3>
<div class="art-linha">
<p class="art-rotulo-linha">Sentenca 001</p>
<p class="art-texto">Hoje o trânsito estava tranquilo.</p>
<div class="art-cols">
<div class="art-col">
<span class="art-col-rot">Original (checkpoint base)</span>
<audio controls preload="none" src="/fala_pb/Inferencias%20finais/Audios/xtts/outputs_final_experiment/original/v3/001.wav"><a href="/fala_pb/Inferencias%20finais/Audios/xtts/outputs_final_experiment/original/v3/001.wav">baixar audio</a></audio>
</div>
<div class="art-col">
<span class="art-col-rot">Ajustado (FALA_PB)</span>
<audio controls preload="none" src="/fala_pb/Inferencias%20finais/Audios/xtts/outputs_final_experiment/ajustado/v2/001.wav"><a href="/fala_pb/Inferencias%20finais/Audios/xtts/outputs_final_experiment/ajustado/v2/001.wav">baixar audio</a></audio>
</div>
</div></div>
<div class="art-linha">
<p class="art-rotulo-linha">Sentenca 003</p>
<p class="art-texto">Depois de muito procurar, finalmente encontrei as chaves que havia perdido durante a mudança.</p>
<div class="art-cols">
<div class="art-col">
<span class="art-col-rot">Original (checkpoint base)</span>
<audio controls preload="none" src="/fala_pb/Inferencias%20finais/Audios/xtts/outputs_final_experiment/original/v1/003.wav"><a href="/fala_pb/Inferencias%20finais/Audios/xtts/outputs_final_experiment/original/v1/003.wav">baixar audio</a></audio>
</div>
<div class="art-col">
<span class="art-col-rot">Ajustado (FALA_PB)</span>
<audio controls preload="none" src="/fala_pb/Inferencias%20finais/Audios/xtts/outputs_final_experiment/ajustado/v3/003.wav"><a href="/fala_pb/Inferencias%20finais/Audios/xtts/outputs_final_experiment/ajustado/v3/003.wav">baixar audio</a></audio>
</div>
</div></div>
<div class="art-linha">
<p class="art-rotulo-linha">Sentenca 012</p>
<p class="art-texto">Quando chegamos ao local do evento, a apresentação já havia começado e quase não encontramos lugares disponíveis.</p>
<div class="art-cols">
<div class="art-col">
<span class="art-col-rot">Original (checkpoint base)</span>
<audio controls preload="none" src="/fala_pb/Inferencias%20finais/Audios/xtts/outputs_final_experiment/original/v3/012.wav"><a href="/fala_pb/Inferencias%20finais/Audios/xtts/outputs_final_experiment/original/v3/012.wav">baixar audio</a></audio>
</div>
<div class="art-col">
<span class="art-col-rot">Ajustado (FALA_PB)</span>
<audio controls preload="none" src="/fala_pb/Inferencias%20finais/Audios/xtts/outputs_final_experiment/ajustado/v1/012.wav"><a href="/fala_pb/Inferencias%20finais/Audios/xtts/outputs_final_experiment/ajustado/v1/012.wav">baixar audio</a></audio>
</div>
</div></div>
<div class="art-linha">
<p class="art-rotulo-linha">Sentenca 036</p>
<p class="art-texto">A praia estava praticamente vazia naquela manhã de terça-feira.</p>
<div class="art-cols">
<div class="art-col">
<span class="art-col-rot">Original (checkpoint base)</span>
<audio controls preload="none" src="/fala_pb/Inferencias%20finais/Audios/xtts/outputs_final_experiment/original/v3/036.wav"><a href="/fala_pb/Inferencias%20finais/Audios/xtts/outputs_final_experiment/original/v3/036.wav">baixar audio</a></audio>
</div>
<div class="art-col">
<span class="art-col-rot">Ajustado (FALA_PB)</span>
<audio controls preload="none" src="/fala_pb/Inferencias%20finais/Audios/xtts/outputs_final_experiment/ajustado/v2/036.wav"><a href="/fala_pb/Inferencias%20finais/Audios/xtts/outputs_final_experiment/ajustado/v2/036.wav">baixar audio</a></audio>
</div>
</div></div>
<div class="art-linha">
<p class="art-rotulo-linha">Sentenca 071</p>
<p class="art-texto">O médico chegou pontualmente.</p>
<div class="art-cols">
<div class="art-col">
<span class="art-col-rot">Original (checkpoint base)</span>
<audio controls preload="none" src="/fala_pb/Inferencias%20finais/Audios/xtts/outputs_final_experiment/original/v2/071.wav"><a href="/fala_pb/Inferencias%20finais/Audios/xtts/outputs_final_experiment/original/v2/071.wav">baixar audio</a></audio>
</div>
<div class="art-col">
<span class="art-col-rot">Ajustado (FALA_PB)</span>
<audio controls preload="none" src="/fala_pb/Inferencias%20finais/Audios/xtts/outputs_final_experiment/ajustado/v3/071.wav"><a href="/fala_pb/Inferencias%20finais/Audios/xtts/outputs_final_experiment/ajustado/v3/071.wav">baixar audio</a></audio>
</div>
</div></div>
</div>
<div class="art-tabela">
<h3>Orpheus TTS</h3>
<div class="art-linha">
<p class="art-rotulo-linha">Sentenca 001</p>
<p class="art-texto">Hoje o trânsito estava tranquilo.</p>
<div class="art-cols">
<div class="art-col">
<span class="art-col-rot">Original (checkpoint base)</span>
<audio controls preload="none" src="/fala_pb/Inferencias%20finais/Audios/unsloth/outputs_final_experiment/original/v3/001.wav"><a href="/fala_pb/Inferencias%20finais/Audios/unsloth/outputs_final_experiment/original/v3/001.wav">baixar audio</a></audio>
</div>
<div class="art-col">
<span class="art-col-rot">Ajustado (FALA_PB)</span>
<audio controls preload="none" src="/fala_pb/Inferencias%20finais/Audios/unsloth/outputs_final_experiment/ajustado/v2/001.wav"><a href="/fala_pb/Inferencias%20finais/Audios/unsloth/outputs_final_experiment/ajustado/v2/001.wav">baixar audio</a></audio>
</div>
</div></div>
<div class="art-linha">
<p class="art-rotulo-linha">Sentenca 003</p>
<p class="art-texto">Depois de muito procurar, finalmente encontrei as chaves que havia perdido durante a mudança.</p>
<div class="art-cols">
<div class="art-col">
<span class="art-col-rot">Original (checkpoint base)</span>
<audio controls preload="none" src="/fala_pb/Inferencias%20finais/Audios/unsloth/outputs_final_experiment/original/v2/003.wav"><a href="/fala_pb/Inferencias%20finais/Audios/unsloth/outputs_final_experiment/original/v2/003.wav">baixar audio</a></audio>
</div>
<div class="art-col">
<span class="art-col-rot">Ajustado (FALA_PB)</span>
<audio controls preload="none" src="/fala_pb/Inferencias%20finais/Audios/unsloth/outputs_final_experiment/ajustado/v2/003.wav"><a href="/fala_pb/Inferencias%20finais/Audios/unsloth/outputs_final_experiment/ajustado/v2/003.wav">baixar audio</a></audio>
</div>
</div></div>
<div class="art-linha">
<p class="art-rotulo-linha">Sentenca 012</p>
<p class="art-texto">Quando chegamos ao local do evento, a apresentação já havia começado e quase não encontramos lugares disponíveis.</p>
<div class="art-cols">
<div class="art-col">
<span class="art-col-rot">Original (checkpoint base)</span>
<audio controls preload="none" src="/fala_pb/Inferencias%20finais/Audios/unsloth/outputs_final_experiment/original/v2/012.wav"><a href="/fala_pb/Inferencias%20finais/Audios/unsloth/outputs_final_experiment/original/v2/012.wav">baixar audio</a></audio>
</div>
<div class="art-col">
<span class="art-col-rot">Ajustado (FALA_PB)</span>
<audio controls preload="none" src="/fala_pb/Inferencias%20finais/Audios/unsloth/outputs_final_experiment/ajustado/v1/012.wav"><a href="/fala_pb/Inferencias%20finais/Audios/unsloth/outputs_final_experiment/ajustado/v1/012.wav">baixar audio</a></audio>
</div>
</div></div>
<div class="art-linha">
<p class="art-rotulo-linha">Sentenca 036</p>
<p class="art-texto">A praia estava praticamente vazia naquela manhã de terça-feira.</p>
<div class="art-cols">
<div class="art-col">
<span class="art-col-rot">Original (checkpoint base)</span>
<audio controls preload="none" src="/fala_pb/Inferencias%20finais/Audios/unsloth/outputs_final_experiment/original/v2/036.wav"><a href="/fala_pb/Inferencias%20finais/Audios/unsloth/outputs_final_experiment/original/v2/036.wav">baixar audio</a></audio>
</div>
<div class="art-col">
<span class="art-col-rot">Ajustado (FALA_PB)</span>
<audio controls preload="none" src="/fala_pb/Inferencias%20finais/Audios/unsloth/outputs_final_experiment/ajustado/v1/036.wav"><a href="/fala_pb/Inferencias%20finais/Audios/unsloth/outputs_final_experiment/ajustado/v1/036.wav">baixar audio</a></audio>
</div>
</div></div>
<div class="art-linha">
<p class="art-rotulo-linha">Sentenca 071</p>
<p class="art-texto">O médico chegou pontualmente.</p>
<div class="art-cols">
<div class="art-col">
<span class="art-col-rot">Original (checkpoint base)</span>
<audio controls preload="none" src="/fala_pb/Inferencias%20finais/Audios/unsloth/outputs_final_experiment/original/v1/071.wav"><a href="/fala_pb/Inferencias%20finais/Audios/unsloth/outputs_final_experiment/original/v1/071.wav">baixar audio</a></audio>
</div>
<div class="art-col">
<span class="art-col-rot">Ajustado (FALA_PB)</span>
<audio controls preload="none" src="/fala_pb/Inferencias%20finais/Audios/unsloth/outputs_final_experiment/ajustado/v2/071.wav"><a href="/fala_pb/Inferencias%20finais/Audios/unsloth/outputs_final_experiment/ajustado/v2/071.wav">baixar audio</a></audio>
</div>
</div></div>
</div>
<div class="art-tabela">
<h3>Fish Speech</h3>
<div class="art-linha">
<p class="art-rotulo-linha">Sentenca 001</p>
<p class="art-texto">Hoje o trânsito estava tranquilo.</p>
<div class="art-cols">
<div class="art-col">
<span class="art-col-rot">Original (checkpoint base)</span>
<audio controls preload="none" src="/fala_pb/Inferencias%20finais/Audios/fishspeech/outputs_final_experiment/original/v2/001.wav"><a href="/fala_pb/Inferencias%20finais/Audios/fishspeech/outputs_final_experiment/original/v2/001.wav">baixar audio</a></audio>
</div>
<div class="art-col">
<span class="art-col-rot">Ajustado (FALA_PB)</span>
<audio controls preload="none" src="/fala_pb/Inferencias%20finais/Audios/fishspeech/outputs_final_experiment/ajustado/v3/001.wav"><a href="/fala_pb/Inferencias%20finais/Audios/fishspeech/outputs_final_experiment/ajustado/v3/001.wav">baixar audio</a></audio>
</div>
</div></div>
<div class="art-linha">
<p class="art-rotulo-linha">Sentenca 003</p>
<p class="art-texto">Depois de muito procurar, finalmente encontrei as chaves que havia perdido durante a mudança.</p>
<div class="art-cols">
<div class="art-col">
<span class="art-col-rot">Original (checkpoint base)</span>
<audio controls preload="none" src="/fala_pb/Inferencias%20finais/Audios/fishspeech/outputs_final_experiment/original/v3/003.wav"><a href="/fala_pb/Inferencias%20finais/Audios/fishspeech/outputs_final_experiment/original/v3/003.wav">baixar audio</a></audio>
</div>
<div class="art-col">
<span class="art-col-rot">Ajustado (FALA_PB)</span>
<audio controls preload="none" src="/fala_pb/Inferencias%20finais/Audios/fishspeech/outputs_final_experiment/ajustado/v2/003.wav"><a href="/fala_pb/Inferencias%20finais/Audios/fishspeech/outputs_final_experiment/ajustado/v2/003.wav">baixar audio</a></audio>
</div>
</div></div>
<div class="art-linha">
<p class="art-rotulo-linha">Sentenca 012</p>
<p class="art-texto">Quando chegamos ao local do evento, a apresentação já havia começado e quase não encontramos lugares disponíveis.</p>
<div class="art-cols">
<div class="art-col">
<span class="art-col-rot">Original (checkpoint base)</span>
<audio controls preload="none" src="/fala_pb/Inferencias%20finais/Audios/fishspeech/outputs_final_experiment/original/v3/012.wav"><a href="/fala_pb/Inferencias%20finais/Audios/fishspeech/outputs_final_experiment/original/v3/012.wav">baixar audio</a></audio>
</div>
<div class="art-col">
<span class="art-col-rot">Ajustado (FALA_PB)</span>
<audio controls preload="none" src="/fala_pb/Inferencias%20finais/Audios/fishspeech/outputs_final_experiment/ajustado/v1/012.wav"><a href="/fala_pb/Inferencias%20finais/Audios/fishspeech/outputs_final_experiment/ajustado/v1/012.wav">baixar audio</a></audio>
</div>
</div></div>
<div class="art-linha">
<p class="art-rotulo-linha">Sentenca 036</p>
<p class="art-texto">A praia estava praticamente vazia naquela manhã de terça-feira.</p>
<div class="art-cols">
<div class="art-col">
<span class="art-col-rot">Original (checkpoint base)</span>
<audio controls preload="none" src="/fala_pb/Inferencias%20finais/Audios/fishspeech/outputs_final_experiment/original/v1/036.wav"><a href="/fala_pb/Inferencias%20finais/Audios/fishspeech/outputs_final_experiment/original/v1/036.wav">baixar audio</a></audio>
</div>
<div class="art-col">
<span class="art-col-rot">Ajustado (FALA_PB)</span>
<audio controls preload="none" src="/fala_pb/Inferencias%20finais/Audios/fishspeech/outputs_final_experiment/ajustado/v1/036.wav"><a href="/fala_pb/Inferencias%20finais/Audios/fishspeech/outputs_final_experiment/ajustado/v1/036.wav">baixar audio</a></audio>
</div>
</div></div>
<div class="art-linha">
<p class="art-rotulo-linha">Sentenca 071</p>
<p class="art-texto">O médico chegou pontualmente.</p>
<div class="art-cols">
<div class="art-col">
<span class="art-col-rot">Original (checkpoint base)</span>
<audio controls preload="none" src="/fala_pb/Inferencias%20finais/Audios/fishspeech/outputs_final_experiment/original/v2/071.wav"><a href="/fala_pb/Inferencias%20finais/Audios/fishspeech/outputs_final_experiment/original/v2/071.wav">baixar audio</a></audio>
</div>
<div class="art-col">
<span class="art-col-rot">Ajustado (FALA_PB)</span>
<audio controls preload="none" src="/fala_pb/Inferencias%20finais/Audios/fishspeech/outputs_final_experiment/ajustado/v2/071.wav"><a href="/fala_pb/Inferencias%20finais/Audios/fishspeech/outputs_final_experiment/ajustado/v2/071.wav">baixar audio</a></audio>
</div>
</div></div>
</div>
<ul class="art-links">
<li><a href="/fala_pb/100/">Catalogo completo dos 1.800 audios</a></li>
<li><a href="/fala_pb/20/">Metodologia e resultados da avaliacao automatica</a></li>
<li><a href="/fala_pb/21/">Validacao perceptual com ouvintes</a></li>
</ul>
</section>

<div class="art-rodape"><p>Os blocos 2 a 7 usam, em boa parte, o mesmo conjunto de cinco frases fixas de acompanhamento, o que permite comparar modelos diretamente entre secoes.</p><p>Os audios sao material de pesquisa academica, gerados no ambito de uma dissertacao de mestrado, e estao disponiveis para fins de verificacao cientifica, ensino e pesquisa. As gravacoes de referencia foram cedidas pelo proprio autor. Ao reutilizar, cite a dissertacao.</p><p><a href="/fala_pb/">Indice de experimentos</a> &middot; <a href="/fala_pb/100/">Catalogo completo das inferencias finais</a></p></div>
