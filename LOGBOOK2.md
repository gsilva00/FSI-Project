# Microsoft SSRS 2012, 2014, 2016 - Remote Code Execution (RCE)

## (Trabalho realizado nas Semanas #2 e #3)

## Identificação

- Existe uma vulnerabilidade no software Microsoft SQL Server Reporting Service (SSRS) com o ID CVE-2020-0618.
- As versões afetadas são SQL Server 2012 Service Pack 2, SQL Server 2014 Service Pack 3 e SQL Server 2016 Systems Service Pack 2.
- Esta vulnerabilidade surge devido ao tratamento incorreto de pedidos HTTP.

## Catalogação

- A [CVE-2020-0618](https://www.cvedetails.com/cve/CVE-2020-0618/) foi descoberta por [Soroush Dalili](https://github.com/irsdl), que elaborou a Prova de Conceito, e [Spencer McIntyre](https://github.com/zeroSteiner), que usou a PdC e elaborou o exploit (módulo Metasploit), a 11/02/2020.
- Este [exploit](https://github.com/rapid7/metasploit-framework/blob/master/modules/exploits/windows/http/ssrs_navcorrector_viewstate.rb) está publicamente disponível no próprio repositório do Metasploit Framework.
- Com um nível de gravidade alto, CVSS de 8.8/10.0, tem um impacto parcial na confidencialidade, integridade e disponibilidade do sistema atacado.

## Exploit

- É um exploit de execução de código remoto (RCE) que executa uma autenticação para aceder ao API do SSRS e envia um pedido POST.
- Este pedido contém um ViewState adulterado que contém código malicioso, que não é verificado (vulnerabilidade) e é desserializado e executado no servidor.
- A automatização permitida pela ferramenta Metasploit destaca-se na criação e codificação do payload ViewState e na distribuição e execução dele, que tem a capacidade de se adaptar ao destino (arquitetura de 32-bit, 64-bit).

## Ataques

- A 18/09/2024 foi adicionada ao Known Exploited Vulnerabilities Catalog da CISA (Cybersecurity and Infrastructure Security Agency), indicando que foi usada para ataques.
- A 29/09/2024, 161041 IPs diferentes foram afetados globalmente por esta vulnerabilidade, com especial incidência nos Estados Unidos, China, Alemanha e Turquia.
- Para além disso, existe uma possibilidade de exploit nos próximos 30 dias de 97,32%.
- Desta forma, embora tenham sido lançadas patches de segurança, sistemas antigos e desatualizados ainda são usados, encontrando-se vulneráveis a este exploit.

## Fontes

- https://www.cve.org/CVERecord?id=CVE-2020-0618
- https://www.cisa.gov/known-exploited-vulnerabilities-catalog
- https://nvd.nist.gov/vuln/detail/CVE-2020-0618
- https://msrc.microsoft.com/update-guide/en-US/advisory/CVE-2020-0618
