# Poker Game (Texas Hold'em)

## Visión general
Este repositorio implementa un motor de Texas Hold'em en Python con soporte para:

- **Motor de juego** con flujo de manos, rondas de apuestas y showdown.
- **Jugadores humanos y bots** con distintos estilos de estrategia.
- **Evaluación de manos** completa (7 cartas → mejor mano de 5 cartas).
- **Cálculo de equity** por Monte Carlo para decisiones del bot.

El objetivo es ofrecer una base clara y extensible para simular partidas de póker y experimentar con lógicas de decisión.

## Estado del proyecto
- **Interfaz actual**: consola (CLI), sin UI gráfica.
- **Dependencias**: no hay dependencias externas (el archivo `requirements.txt` está vacío).
- **Alcance**: Texas Hold'em, 2+ jugadores, con manejo de ciegas y side pots.

## Ejecución rápida
1. Asegúrate de usar Python 3.10+.
2. Ejecuta el punto de entrada:

```bash
python main.py
```

Se inicia una mesa con 1 humano y 3 bots con estilos distintos. El flujo es interactivo por consola.

## Arquitectura y componentes clave
La lógica del juego se divide en módulos independientes, para mantener el motor desacoplado de los jugadores y los cálculos de manos.

### `main.py`
- **Responsabilidad**: punto de entrada y orquestación de la partida.
- Crea 4 jugadores (`HumanPlayer` + 3 `BotPlayer`).
- Instancia `PokerEngine` con stacks iniciales.
- Mantiene el loop principal: inicia manos, pide acciones, imprime el estado y pregunta si continuar.

### `poker/engine.py` — Motor del juego
- **Responsabilidad**: reglas del juego, flujo de mano, validación de acciones y distribución de pot.
- Funciones clave:
  - `start_hand()`: baraja, reparte, inicializa estado y postea ciegas.
  - `apply_action()`: valida y aplica acciones (fold/call/check/raise), administra apuestas y transiciones de ronda.
  - `advance_street()`: avanza `preflop → flop → turn → river → showdown`.
  - `resolve_showdown()`: evalúa manos, reparte main pot y side pots.
- Maneja **side pots** y **all-in**, además de la rotación del dealer.

### `poker/game_state.py` — Estado de la mano
- **Responsabilidad**: contenedor de estado mutable para la mano actual.
- Incluye:
  - stacks, apuestas, pot, street actual, board, manos privadas
  - jugadores activos, all-ins, historial de acciones
  - contribuciones totales por jugador para cálculos de side pots
- Métodos utilitarios: `to_call`, `reset_betting_round`, `compute_side_pots`.

### `poker/actions.py` — Modelo de acciones
- **ActionType**: `FOLD`, `CHECK`, `CALL`, `RAISE`.
- **Action**: dataclass inmutable con tipo y monto opcional (para raises).

### `poker/players/`
- **`BasePlayer`**: interfaz mínima, solo define `decide()`.
- **`HumanPlayer`**:
  - Entrada interactiva en consola.
  - Restringe acciones permitidas según si hay que pagar o no.
- **`BotPlayer`**:
  - Implementa decisión basada en estilo (`tight`, `loose`, `aggro`, etc.).
  - Usa heurísticas preflop y evaluación en postflop.
  - Calcula equity con Monte Carlo para decisiones marginales.

### `poker/hand_evaluator.py` — Evaluación de manos
- Evalúa 7 cartas y elige la mejor combinación de 5.
- Ranking completo desde `HIGH_CARD` hasta `STRAIGHT_FLUSH`.
- Considera escaleras con As bajo (`A-2-3-4-5`).

### `poker/monte_carlo.py` — Estimación de equity
- Genera escenarios aleatorios para completar mesa y oponente.
- Calcula probabilidad aproximada de victoria/empate del héroe.
- Usado por los bots para decisiones en postflop.

### `poker/cards.py` y `poker/deck.py`
- **`Card`**: dataclass inmutable con validación de rango y palo.
- **`Deck`**: baraja estándar, soporte de `shuffle()` y `deal()`.

## Flujo de una mano (alto nivel)
1. **Inicio** (`start_hand`): se baraja, se reparte, se postean ciegas.
2. **Preflop**: se solicita acción a cada jugador en orden.
3. **Flop / Turn / River**: se revelan cartas comunitarias y se repite la ronda de apuestas.
4. **Showdown**:
   - Se evalúan manos activas.
   - Se reparten pots y side pots.
   - Se actualizan stacks y se rota el dealer.

## Estilos de bots
Los bots cuentan con un perfil configurable que ajusta:
- **Tightness preflop**: cuántas manos iniciales juega.
- **Agresión**: propensión a subir en lugar de pagar.
- **Bluff frequency**: actualmente está fijado en 0.0 (sin faroles).
- **Equity threshold**: sesgo al decidir si pagar en postflop.

Estilos predefinidos:
- `balanced`, `tight`, `loose`, `aggro`, `passive`

## Limitaciones actuales
- No hay separación de main pot y side pots en pantalla más allá del resumen impreso.
- No hay persistencia de partidas ni log histórico.
- La lógica de bots es heurística básica; no hay árboles de decisión ni ICM.
- No existe interfaz gráfica o API.

## Cómo extender el proyecto
Algunas extensiones naturales que mantienen la arquitectura limpia:
- **Mejorar bots**:
  - usar rangos preflop más realistas
  - introducir bluffing y sizing dinámico
- **UI o API**:
  - agregar una interfaz web o TUI sobre `PokerEngine`
- **Tests**:
  - unit tests para `hand_evaluator` y `compute_side_pots`
- **Soporte multi-mesa**:
  - orquestar varias instancias del motor con configuraciones distintas

## Estructura del repositorio
```
.
├── main.py
├── poker/
│   ├── engine.py
│   ├── game_state.py
│   ├── actions.py
│   ├── hand_evaluator.py
│   ├── monte_carlo.py
│   ├── cards.py
│   ├── deck.py
│   └── players/
│       ├── base_player.py
│       ├── human_player.py
│       └── bot_player.py
└── requirements.txt
```

## Buenas prácticas recomendadas
- Mantener `PokerEngine` como fuente única de verdad del estado.
- Encapsular nuevas decisiones en jugadores, no en el motor.
- Evitar imprimir en clases de dominio si se quiere migrar a UI/API.
- Cubrir con pruebas el evaluador de manos antes de cambiarlo.

---

Si necesitas que incorporemos UI, modo torneo, multi-mesa o entrenamiento de bots, se puede priorizar en el siguiente ciclo.
