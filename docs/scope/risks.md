# Gestão de Riscos

**Projecto:** Musical Theory Trainer  
**Versão:** 1.0 · 28/08/2026

---

## Tabela de riscos

| ID | Risco | Probabilidade | Impacto | Mitigação |
|----|-------|--------------|---------|-----------|
| R01 | Introdução de erros ao conceber e implementar o Modelo de Teoria Musical  | Média | Alto | Validação da conceção e implementação do modelo com base em referências de teoria musical; Testes unitários a todo o modelo implementado de forma a detetar erros capazes de afetar a correção dos exercícios gerados.|
| R02 | O gerador de exercícios produz exercícios inválidos apesar de um modelo de teoria correto  | Média | Alto | Definição de algoritmos com regras e restrições adequadas; Testes unitários e de integração do componente responsável pela geração, de forma a avaliar a correção dos exercícios gerados|
| R03 | Níveis de dificuldade desajustados para os exercícios |Média | Médio |Validação dos níveis de dificuldade conceptualizados com o auxilio de referências de teoria musical. Testes de usabilidade aos vários tipos de exercícios configurados com vários níveis de dificuldade.|
| R04 | Latência elevada ou problemas na comunicação com dispositivos MIDI | Média | Alto | Realização de testes de desempenho, unitários e de integração do módulo responsável pela comunicação com dispositivos MIDI de forma a avaliar a latência e correto funcionamento do módulo; Implementação de tratamento de erros adequada para lidar com problemas de conexão |
| R05 | Latência elevada ou problemas na síntese e reprodução de áudio |Média | Alto | Realização de testes de desempenho, unitários e de integração ao módulo responsável pela síntese e reprodução de áudio de forma a avaliar a latência, qualidade do áudio e correto funcionamento do módulo|
---
