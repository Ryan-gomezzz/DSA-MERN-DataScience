# Embedded C Study Guide: From C Basics to Microcontroller Firmware

This guide teaches the C language and hardware concepts needed to write reliable embedded programs. It also explains how to compile and run ordinary C programs on your current Windows computer.

> **Important distinction:** a desktop C program is compiled for Windows and runs as an `.exe`. An embedded program is cross-compiled for a particular microcontroller, flashed into that device, and usually has no operating system, terminal, or standard output.

## 1. Run a C Program on Windows

Your `hello.c` should be:

```c
#include <stdio.h>

int main(void)
{
    printf("Hello, World!\n");
    return 0;
}
```

Why each part matters:

- `<stdio.h>` declares `printf`.
- `int main(void)` explicitly says that `main` takes no arguments.
- `\n` prints a newline.
- `return 0` reports successful completion to the operating system.

Your machine currently finds Clang, so open PowerShell in the repository and run:

```powershell
cd C:\Users\ryang\OneDrive\Desktop\DSA\c\embeddedC
clang -std=c17 -Wall -Wextra -Wpedantic hello.c -o hello.exe
.\hello.exe
```

Expected output:

```text
Hello, World!
```

The commands mean:

- `clang`: run the compiler driver.
- `-std=c17`: use the C17 language standard.
- `-Wall -Wextra -Wpedantic`: enable useful warnings.
- `hello.c`: input source file.
- `-o hello.exe`: output executable name.
- `.\hello.exe`: run that executable from the current PowerShell directory.

If `clang` compiles but cannot link a Windows executable, install one complete desktop toolchain:

- **Visual Studio Build Tools:** install the “Desktop development with C++” workload, open its Developer PowerShell, and use `cl /W4 hello.c` followed by `.\hello.exe`.
- **MSYS2/MinGW-w64:** install GCC through MSYS2, then use `gcc -std=c17 -Wall -Wextra -Wpedantic hello.c -o hello.exe`.

Do not download a random `gcc.exe` alone. A working toolchain also needs headers, libraries, assembler, and linker support.

### Compile only, without running

Check syntax and warnings:

```powershell
clang -std=c17 -Wall -Wextra -Wpedantic -fsyntax-only hello.c
```

Create an object file but do not link:

```powershell
clang -std=c17 -Wall -Wextra -c hello.c -o hello.obj
```

### Debug versus optimized builds

```powershell
# Debug-friendly build
clang -std=c17 -Wall -Wextra -Wpedantic -g -O0 hello.c -o hello.exe

# Optimized release build
clang -std=c17 -Wall -Wextra -Wpedantic -O2 hello.c -o hello.exe
```

- `-g` stores debug information.
- `-O0` makes debugging easier.
- `-O2` enables useful optimization.
- Treat warnings seriously; add `-Werror` in controlled builds when warning-free code is expected.

### Multiple source files

```text
main.c
gpio.c
gpio.h
```

Compile and link together:

```powershell
clang -std=c17 -Wall -Wextra -Wpedantic main.c gpio.c -o app.exe
.\app.exe
```

Or build separately:

```powershell
clang -std=c17 -Wall -Wextra -c main.c -o main.obj
clang -std=c17 -Wall -Wextra -c gpio.c -o gpio.obj
clang main.obj gpio.obj -o app.exe
```

## 2. How Embedded Programs Run

A typical embedded workflow is:

```text
C source and headers
        |
        v
Cross-compiler -> object files -> linker + linker script
        |                         |
        +-------------------------+
                    |
                    v
        ELF debug image + BIN/HEX firmware
                    |
                    v
       Debug probe / bootloader / programmer
                    |
                    v
             Microcontroller flash
                    |
                    v
         Reset -> startup -> main loop/RTOS
```

You need tools matching the target:

- ARM Cortex-M: often `arm-none-eabi-gcc`, Clang/LLVM, or a vendor IDE/toolchain
- AVR: often `avr-gcc` and `avrdude`
- ESP32: Espressif ESP-IDF toolchain
- RP2040: Raspberry Pi Pico SDK toolchain
- Vendor boards: STM32CubeIDE, MPLAB X, TI Code Composer Studio, and others

`clang hello.c` on Windows builds for the computer, not automatically for a microcontroller. Embedded compilation needs the target CPU, ABI, device startup code, linker script, headers, and usually a board support package.

Typical ARM commands, only as a conceptual example:

```powershell
arm-none-eabi-gcc -mcpu=cortex-m4 -mthumb -O2 -g `
  -ffreestanding -Wall -Wextra `
  startup.c main.c -T device.ld -o firmware.elf

arm-none-eabi-objcopy -O ihex firmware.elf firmware.hex
arm-none-eabi-size firmware.elf
```

Exact flags must match the microcontroller. Never copy CPU, floating-point, memory-map, or flash commands from a different device.

## 3. What Makes Embedded C Different?

Embedded C is C used under hardware constraints. The language is mostly the same, but the environment is different:

- Direct access to memory-mapped hardware registers
- Limited RAM, flash, CPU time, and electrical power
- No operating system on many systems
- Startup begins from reset, not a desktop process loader
- Interrupts and concurrent hardware events
- Timing deadlines and real-time behavior
- Device-specific toolchains, headers, and linker scripts
- Cross-compilation: build on one machine for another CPU
- Hardware failures and safety consequences

A **host** is the computer building/debugging the program. A **target** is the microcontroller running the firmware.

## 4. Number Systems and Binary Fundamentals

Embedded programming constantly uses binary and hexadecimal.

```c
uint8_t binary_value = 0b10100101; /* Supported by C23; extension in older C. */
uint8_t hex_value = 0xA5U;         /* Portable in older C standards. */
uint8_t octal_value = 0245U;
```

Hex maps neatly to binary because one hex digit represents four bits:

```text
0xA5 = 1010 0101
         A    5
```

For an unsigned `n`-bit integer:

```text
minimum = 0
maximum = 2^n - 1
```

An 8-bit unsigned value ranges from 0 through 255. Signed integer representation is almost universally two's complement; fixed-width types make intended widths clear.

Units:

- 1 bit: binary 0 or 1
- 1 byte: `CHAR_BIT` bits, almost always 8 on current embedded targets
- KiB: 1024 bytes
- MiB: 1024 KiB

Use `sizeof` instead of assuming type sizes.

## 5. Core C Types for Embedded Work

The built-in types include:

```c
char
short
int
long
long long
float
double
_Bool
```

Their exact widths can vary by target. Prefer `<stdint.h>` when width matters:

```c
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

uint8_t byte_value;
int16_t signed_sample;
uint32_t timer_count;
int32_t position;
bool enabled;
size_t buffer_length;
```

Other useful types:

- `uint_least16_t`: smallest available unsigned type with at least 16 bits
- `uint_fast16_t`: fastest available unsigned type with at least 16 bits
- `uintptr_t`: unsigned integer capable of holding a converted data pointer, when provided
- `intmax_t` and `uintmax_t`: widest standard integer types

Use suffixes to make literal intent clear:

```c
uint32_t timeout_ms = 1000UL;
float gain = 0.25F;
```

### Integer promotions and conversion traps

Small integer types are often promoted to `int` during arithmetic. Mixing signed and unsigned values can produce surprising comparisons.

```c
uint16_t a = 50000U;
uint16_t b = 2U;
uint32_t product = (uint32_t)a * (uint32_t)b;
```

Cast before multiplication when the intermediate must be wider. Casting only after overflow is too late.

Avoid casual comparisons such as:

```c
int count = -1;
uint32_t limit = 10U;

/* count < limit may not mean what a beginner expects after conversion. */
```

Compile with strong warnings and keep signedness consistent.

## 6. Variables, Scope, Storage Duration, and Linkage

### Local automatic variable

```c
void update(void)
{
    uint32_t temporary = 0U;
}
```

It normally exists until the block exits and is often stored on the stack or in registers.

### Static local variable

```c
uint32_t next_sequence(void)
{
    static uint32_t sequence = 0U;
    return sequence++;
}
```

It retains its value across calls and has static storage duration.

### File-private object or function

```c
static uint8_t driver_state;

static void reset_driver_state(void)
{
    driver_state = 0U;
}
```

At file scope, `static` gives internal linkage, hiding the name from other translation units. Use it for module encapsulation.

### Shared declaration with `extern`

Header:

```c
extern volatile uint32_t system_ticks;
```

Exactly one source file:

```c
volatile uint32_t system_ticks = 0U;
```

Prefer functions over widely shared global variables.

## 7. Operators and Control Flow

Arithmetic:

```c
+  -  *  /  %
```

Comparison and logical operators:

```c
==  !=  <  <=  >  >=
&&  ||  !
```

Bitwise operators:

```c
&  |  ^  ~  <<  >>
```

Do not confuse:

- `=` assignment with `==` comparison
- `&` bitwise AND with `&&` logical AND
- `|` bitwise OR with `||` logical OR

Control flow:

```c
if (temperature > limit) {
    shut_down();
} else {
    continue_operation();
}

switch (state) {
case STATE_IDLE:
    handle_idle();
    break;
case STATE_ACTIVE:
    handle_active();
    break;
default:
    handle_fault();
    break;
}
```

Loops:

```c
for (size_t i = 0U; i < length; ++i) {
    process(data[i]);
}

while (!ready()) {
    service_watchdog();
}

do {
    sample = read_sensor();
} while (sample_is_invalid(sample));
```

Every embedded loop should have a clear exit, timing behavior, or deliberate infinite-loop design.

## 8. Functions and APIs

Declare functions before use:

```c
uint16_t clamp_u16(uint16_t value, uint16_t low, uint16_t high);

uint16_t clamp_u16(uint16_t value, uint16_t low, uint16_t high)
{
    if (value < low) {
        return low;
    }
    if (value > high) {
        return high;
    }
    return value;
}
```

Use `void` explicitly for no parameters:

```c
void initialize(void);
```

Pass output through pointers when needed:

```c
typedef enum {
    STATUS_OK,
    STATUS_INVALID_ARGUMENT,
    STATUS_TIMEOUT
} status_t;

status_t sensor_read(uint16_t *result)
{
    if (result == NULL) {
        return STATUS_INVALID_ARGUMENT;
    }

    *result = 123U;
    return STATUS_OK;
}
```

A useful embedded API makes ownership, valid ranges, units, blocking behavior, error behavior, and interrupt safety clear.

## 9. Arrays, Strings, Structures, and Enums

### Arrays

```c
uint16_t samples[16] = {0U};
size_t count = sizeof samples / sizeof samples[0];
```

Arrays decay to pointers in most function calls, so pass the length separately:

```c
uint32_t sum_u16(const uint16_t *values, size_t length)
{
    uint32_t total = 0U;
    for (size_t i = 0U; i < length; ++i) {
        total += values[i];
    }
    return total;
}
```

### Strings

A C string is a character array terminated by `\0`.

```c
char name[] = "sensor";       /* Seven bytes including terminator. */
const char *label = "ADC0";   /* Do not modify the string literal. */
```

Buffer sizes must include the terminator. Functions such as `sprintf`, `strcpy`, and unchecked input can overflow buffers. Prefer bounded operations and verify truncation/error behavior.

```c
#include <stdio.h>

char message[32];
int written = snprintf(message, sizeof message, "ADC=%u", (unsigned)value);
if ((written < 0) || ((size_t)written >= sizeof message)) {
    /* Formatting failed or output was truncated. */
}
```

Some bare-metal C libraries omit or greatly enlarge formatted I/O. Avoid `printf` in small production firmware unless its cost is understood.

### Structures

```c
typedef struct {
    uint16_t raw;
    int32_t millivolts;
    bool valid;
} adc_sample_t;
```

The compiler may insert padding for alignment. Do not assume `sizeof(struct)` equals the sum of member sizes.

### Enumerations

```c
typedef enum {
    MOTOR_STOPPED,
    MOTOR_STARTING,
    MOTOR_RUNNING,
    MOTOR_FAULT
} motor_state_t;
```

Enums make states more readable, but the underlying size is implementation-defined unless controlled by compiler options/extensions. Do not use an ordinary enum as a fixed-width wire format.

### Unions

Unions overlay members in the same storage:

```c
typedef union {
    uint32_t word;
    uint8_t bytes[4];
} word_view_t;
```

Union type-punning, endianness, padding, and aliasing rules can reduce portability. `memcpy` is often the clearest portable way to copy between object representations.

## 10. Pointers

A pointer stores an address:

```c
uint16_t value = 42U;
uint16_t *pointer = &value;
*pointer = 100U;
```

Key operations:

- `&object`: address of object
- `*pointer`: object at the pointed-to address
- `pointer + 1`: advances by the size of the pointed-to type
- `NULL`: no valid object address

Qualify the pointed-to object and pointer separately:

```c
const uint8_t *p1;             /* Pointer to read-only data. */
uint8_t * const p2 = buffer;   /* Fixed pointer to writable data. */
const uint8_t * const p3 = rom_table; /* Both fixed and read-only. */
```

Common pointer bugs:

- Null dereference
- Uninitialized or wild pointer
- Out-of-bounds access
- Use after lifetime ends
- Incorrect cast/alignment
- Returning the address of a local automatic variable
- Losing ownership of dynamically allocated memory

On many microcontrollers, invalid memory access causes a fault exception or silent corruption.

## 11. The Essential Qualifiers

### `const`

`const` means code through that access path must not modify the object:

```c
uint16_t average(const uint16_t *samples, size_t count);
```

It documents intent and can enable placement in read-only memory, but it does not mean a value can never change through another alias or hardware.

### `volatile`

`volatile` tells the compiler that an object's value may change outside the normal visible flow and that accesses are observable.

Typical uses:

- Memory-mapped I/O registers
- Variables changed by an interrupt and read by normal code
- Variables changed by hardware/DMA

```c
static volatile bool transfer_done;
```

What `volatile` does **not** provide:

- Atomicity
- Thread safety
- Mutual exclusion
- Memory ordering between CPUs
- Protection from race conditions
- A general replacement for synchronization

### `restrict`

For suitable C APIs, `restrict` promises that pointed-to objects do not overlap through competing aliases during the relevant execution. This can enable optimization, but violating the promise causes undefined behavior.

```c
void add_arrays(float *restrict out,
                const float *restrict a,
                const float *restrict b,
                size_t length);
```

Use it only when the aliasing contract is guaranteed.

## 12. Bit Manipulation

Bit operations control registers and packed fields.

```c
#include <stdint.h>

#define BIT(position) (UINT32_C(1) << (position))

uint32_t flags = 0U;

flags |= BIT(3);          /* Set bit 3. */
flags &= ~BIT(3);         /* Clear bit 3. */
flags ^= BIT(3);          /* Toggle bit 3. */
bool is_set = (flags & BIT(3)) != 0U;
```

Update a multi-bit field:

```c
#define MODE_POSITION 4U
#define MODE_MASK     (UINT32_C(3) << MODE_POSITION)

register_value = (register_value & ~MODE_MASK)
               | ((new_mode << MODE_POSITION) & MODE_MASK);
```

Extract a field:

```c
uint32_t mode = (register_value & MODE_MASK) >> MODE_POSITION;
```

Shift cautions:

- Do not shift by a negative value or by the type width or more.
- Left-shifting a signed value into overflow is undefined behavior.
- Right-shifting a negative signed value is implementation-defined.
- Use unsigned values for register bit operations.
- Parenthesize macro parameters and expressions.

## 13. Preprocessor, Headers, and Modules

### Header guard

```c
#ifndef GPIO_H
#define GPIO_H

#include <stdbool.h>
#include <stdint.h>

void gpio_initialize(void);
void gpio_write(uint32_t pin, bool high);

#endif
```

Put declarations, types, constants, and API documentation in headers. Put definitions and private details in source files.

### Safe macros

```c
#define ARRAY_LENGTH(array) (sizeof(array) / sizeof((array)[0]))
#define MAX_TIMEOUT_MS UINT32_C(5000)
```

Beware of macro arguments evaluated multiple times:

```c
#define BAD_MAX(a, b) ((a) > (b) ? (a) : (b))
/* BAD_MAX(i++, j++) can change one operand twice. */
```

Prefer `static inline` functions when type checking and single evaluation matter:

```c
static inline uint16_t min_u16(uint16_t a, uint16_t b)
{
    return (a < b) ? a : b;
}
```

Conditional compilation:

```c
#if defined(BOARD_REV_B)
    /* Revision B implementation. */
#else
    /* Default implementation. */
#endif
```

Keep board differences in a small hardware-abstraction layer instead of spreading conditionals everywhere.

## 14. Memory Layout

A linked embedded image commonly contains:

| Section | Typical contents | Initial location |
|---|---|---|
| `.text` | Executable instructions | Flash/ROM |
| `.rodata` | Read-only constants | Flash/ROM |
| `.data` | Initialized writable globals/statics | Initial values in flash, runtime copies in RAM |
| `.bss` | Zero-initialized globals/statics | RAM; cleared during startup |
| Stack | Calls, saved registers, many local variables | RAM |
| Heap | Dynamic allocation | RAM, if used |

```c
const uint16_t table[] = {1U, 2U, 3U}; /* Usually read-only memory. */
uint32_t initialized = 5U;             /* .data */
uint32_t zero_initialized;             /* .bss */
```

The linker script defines exact memory regions and section placement. The startup code normally:

1. Sets the initial stack pointer.
2. Copies initialized `.data` values from flash to RAM.
3. Clears `.bss`.
4. Initializes runtime/system state.
5. Calls `main`.

### Stack safety

Embedded stacks are small. Risks include:

- Deep call chains
- Recursion
- Large local arrays
- Nested interrupts
- Large library functions

Avoid uncontrolled recursion. Measure worst-case stack use with tool support, static analysis, or stack watermarking.

### Dynamic allocation

`malloc` and `free` can cause fragmentation, unpredictable timing, allocation failure, and ownership bugs. Many embedded systems avoid dynamic allocation after initialization.

Alternatives:

- Fixed-size arrays
- Static object pools
- Ring buffers
- Region/arena allocation during initialization
- Explicit maximum capacities

## 15. Memory-Mapped I/O and Registers

Peripherals expose registers at fixed addresses. Vendor headers normally provide correct definitions; use them instead of inventing addresses.

A simplified educational example:

```c
#include <stdint.h>

#define GPIO_OUT_ADDRESS UINT32_C(0x40020014)
#define GPIO_OUT (*(volatile uint32_t *)GPIO_OUT_ADDRESS)

void led_on(void)
{
    GPIO_OUT |= (UINT32_C(1) << 5U);
}
```

The address and bit position are device-specific and may be wrong for your hardware. Consult the exact datasheet/reference manual.

Register access has special behavior:

- Some bits are read-only.
- Some clear when read.
- Some clear when a `1` is written.
- Some fields require an unlock sequence.
- Reserved bits must retain documented values.
- A read-modify-write may race with hardware or an interrupt.

Always read the register's description, reset value, access type, and timing rules.

## 16. Endianness, Alignment, and Representation

Endianness is byte order for multi-byte values:

- Little-endian stores the least-significant byte at the lowest address.
- Big-endian stores the most-significant byte at the lowest address.

Do not serialize by sending a struct's raw memory. Padding, endianness, type widths, and compiler ABI can differ.

Encode explicitly:

```c
void write_u16_be(uint8_t out[2], uint16_t value)
{
    out[0] = (uint8_t)(value >> 8U);
    out[1] = (uint8_t)(value & UINT16_C(0x00FF));
}

uint16_t read_u16_be(const uint8_t in[2])
{
    return (uint16_t)(((uint16_t)in[0] << 8U) | (uint16_t)in[1]);
}
```

Some CPUs fault or slow down on misaligned access. Do not cast arbitrary byte-buffer addresses to wider pointer types. Decode bytes or use `memcpy` where appropriate.

## 17. GPIO

General-purpose input/output pins usually require:

1. Enable the peripheral clock.
2. Select GPIO function instead of an alternate function.
3. Configure direction.
4. Configure pull-up/pull-down, drive strength, and output type.
5. Read input or write output.

Pseudo-API:

```c
gpio_configure_output(LED_PIN);
gpio_write(LED_PIN, true);

gpio_configure_input(BUTTON_PIN, GPIO_PULL_UP);
bool pressed = !gpio_read(BUTTON_PIN); /* Active-low button. */
```

Electrical facts matter:

- Do not exceed voltage/current ratings.
- An unconnected input may float.
- Push-pull and open-drain outputs behave differently.
- LEDs and buttons may be active-low.
- Mechanical buttons bounce.

### Debouncing

Do not treat the first electrical transition as a clean press. A non-blocking debounce strategy accepts a new state only after it remains stable for a time interval.

```c
typedef struct {
    bool stable_state;
    bool candidate_state;
    uint32_t candidate_since_ms;
} debounce_t;
```

Avoid a long busy-wait delay because it prevents other work.

## 18. Super Loop and State Machines

A basic bare-metal architecture:

```c
int main(void)
{
    hardware_initialize();

    for (;;) {
        read_inputs();
        update_state_machine();
        update_outputs();
        service_communications();
        service_watchdog();
    }
}
```

Use a state machine for behavior that evolves across events:

```c
typedef enum {
    STATE_OFF,
    STATE_STARTING,
    STATE_RUNNING,
    STATE_FAULT
} state_t;

static state_t state = STATE_OFF;

void controller_step(void)
{
    switch (state) {
    case STATE_OFF:
        if (start_requested()) {
            begin_startup();
            state = STATE_STARTING;
        }
        break;

    case STATE_STARTING:
        if (fault_detected()) {
            state = STATE_FAULT;
        } else if (startup_complete()) {
            state = STATE_RUNNING;
        }
        break;

    case STATE_RUNNING:
        if (fault_detected()) {
            state = STATE_FAULT;
        } else if (stop_requested()) {
            stop_outputs();
            state = STATE_OFF;
        }
        break;

    case STATE_FAULT:
        make_outputs_safe();
        if (fault_reset_requested()) {
            state = STATE_OFF;
        }
        break;

    default:
        make_outputs_safe();
        state = STATE_FAULT;
        break;
    }
}
```

State machines are explicit, testable, and non-blocking.

## 19. Time Without Blocking

Instead of delaying inside a loop, compare timestamps:

```c
static uint32_t last_run_ms;

void scheduler_step(uint32_t now_ms)
{
    if ((uint32_t)(now_ms - last_run_ms) >= 100U) {
        last_run_ms = now_ms;
        sample_sensor();
    }
}
```

Unsigned subtraction makes this idiom work correctly across counter wraparound, as long as intervals are below the relevant half/full range required by the design.

Avoid this fragile pattern:

```c
if (now_ms >= last_run_ms + 100U) {
    /* Addition may wrap. */
}
```

## 20. Interrupts

An interrupt temporarily transfers execution to an interrupt service routine (ISR).

Good ISR rules:

- Keep it short and bounded.
- Acknowledge/clear the correct interrupt source.
- Capture necessary data.
- Set a flag or enqueue work for normal context.
- Avoid blocking, dynamic allocation, and heavy formatting.
- Avoid calling code that is not interrupt-safe.

Conceptual example:

```c
static volatile bool sample_ready;
static volatile uint16_t latest_sample;

void ADC_IRQHandler(void)
{
    latest_sample = ADC_RESULT_REGISTER;
    sample_ready = true;
    ADC_CLEAR_INTERRUPT();
}

void application_step(void)
{
    if (sample_ready) {
        uint16_t sample;

        disable_interrupts();
        sample = latest_sample;
        sample_ready = false;
        enable_interrupts();

        process_sample(sample);
    }
}
```

Actual ISR names, register actions, and critical-section functions are platform-specific.

### Atomicity and races

An access can be non-atomic when the object is wider than the CPU's natural access or when a read-modify-write operation is interrupted.

```c
counter++; /* Read, add, write: not automatically atomic. */
```

Protect shared state using an appropriate mechanism:

- Brief interrupt masking
- Atomic instructions/types supported by target and toolchain
- RTOS mutex/semaphore for task context
- Single-producer/single-consumer queue design
- Snapshot/copy protocols

Keep critical sections short and account for interrupt latency.

## 21. Ring Buffers

Ring buffers are useful for UART and sampled data.

```c
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

#define RX_CAPACITY 16U

typedef struct {
    uint8_t data[RX_CAPACITY];
    size_t head;
    size_t tail;
} ring_buffer_t;

bool ring_push(ring_buffer_t *buffer, uint8_t value)
{
    size_t next = (buffer->head + 1U) % RX_CAPACITY;
    if (next == buffer->tail) {
        return false; /* Full; one slot remains unused. */
    }

    buffer->data[buffer->head] = value;
    buffer->head = next;
    return true;
}

bool ring_pop(ring_buffer_t *buffer, uint8_t *value)
{
    if (buffer->head == buffer->tail) {
        return false;
    }

    *value = buffer->data[buffer->tail];
    buffer->tail = (buffer->tail + 1U) % RX_CAPACITY;
    return true;
}
```

Concurrency still matters if an ISR and main context access it. Decide ownership of each index and use atomic/protected access appropriate to the target.

## 22. Timers, Counters, Capture, and PWM

Hardware timers count clock ticks and can provide:

- Periodic interrupts
- One-shot timeouts
- Input capture for measuring edges/pulse widths
- Output compare for scheduled pin changes
- PWM generation
- Encoder counting

Basic relationship:

```text
timer tick frequency = timer input clock / prescaler
period = timer counts / timer tick frequency
```

For edge-aligned PWM:

```text
PWM frequency approximately = timer clock / (prescaler * period counts)
duty cycle = compare counts / period counts
```

Check the device manual for off-by-one behavior, center alignment, clock multipliers, preload registers, and update events.

## 23. ADC and DAC

An ADC converts voltage to a digital code. For an ideal unsigned N-bit ADC:

```text
code range = 0 through (2^N - 1)
voltage approximately = code * Vref / (2^N - 1)
```

Real measurements depend on:

- Reference accuracy and noise
- Input range
- Source impedance and sampling time
- Resolution versus effective number of bits
- Offset/gain error
- Quantization and electrical noise
- Calibration

Use a wide intermediate:

```c
uint32_t adc_to_millivolts(uint16_t code, uint32_t reference_mv)
{
    return ((uint32_t)code * reference_mv) / UINT32_C(4095);
}
```

A DAC performs the inverse idea. PWM plus a filter can sometimes provide an approximate analog output.

## 24. UART, SPI, and I2C

### UART

Asynchronous serial communication uses transmit, receive, and agreed settings:

- Baud rate
- Data bits
- Parity
- Stop bits
- Voltage levels

UART does not inherently define message boundaries or reliability. Design a protocol with length or delimiters, validation, timeouts, and recovery.

### SPI

Synchronous, usually full-duplex:

- SCLK: clock
- MOSI: controller to peripheral
- MISO: peripheral to controller
- CS: chip select

Both sides must agree on clock polarity/phase, bit order, frequency, and transaction framing. “Read” often requires transmitting dummy bytes because transmit and receive occur together.

### I2C

Two-wire addressed bus:

- SDA: data
- SCL: clock
- Open-drain lines with pull-up resistors
- Address, ACK/NACK, start/stop conditions

Handle bus busy, NACK, timeouts, arbitration where relevant, and stuck-bus recovery. A displayed “8-bit I2C address” may include the read/write bit; many APIs expect the 7-bit address.

### Protocol design

A robust packet might include:

```text
preamble | version | message type | length | sequence | payload | CRC
```

Define endianness, maximum length, timeout, escaping/framing, retransmission policy, version compatibility, and malformed-input behavior.

## 25. DMA

Direct memory access moves data between peripherals and memory with limited CPU involvement.

Typical uses:

- ADC sample buffers
- UART/SPI transmit and receive
- Audio streams
- Memory copies

DMA introduces concurrency:

- A buffer may change while the CPU reads it.
- Cache maintenance may be required on cached processors.
- Alignment and accessible memory regions matter.
- Completion/half-completion interrupts need correct ownership.

Use double buffering or explicit buffer states so hardware and software never own the same region simultaneously.

## 26. Watchdogs, Reset, and Fault Handling

A watchdog resets the system if software fails to service it within a window. Do not feed it blindly from a timer ISR; feed it only when critical tasks have demonstrated progress.

At startup, record reset cause when hardware provides it:

- Power-on reset
- External reset
- Watchdog reset
- Brownout
- Software reset
- Fault/lockup

Fault strategy:

1. Put outputs into a safe state.
2. Capture compact diagnostic information if safe.
3. Avoid repeatedly corrupting persistent data.
4. Reset or enter a controlled fault mode.
5. Prevent endless reset loops when possible.

Assertions are useful during development:

```c
#include <assert.h>

assert(buffer != NULL);
```

Production assertion behavior must be deliberately designed. A silent removal of all checks may be unsafe; an uncontrolled halt may also be unsafe.

## 27. Power and Clock Management

Power-saving methods include:

- Disable unused peripheral clocks.
- Reduce clock frequency/voltage when supported.
- Sleep while waiting instead of busy polling.
- Batch radio or sensor activity.
- Use timer/GPIO/RTC wake sources.
- Put external devices into low-power modes.

After wake-up, clocks and peripherals may need reinitialization or stabilization delays. Debug connections can prevent the lowest-power modes, so measure on real hardware with suitable equipment.

## 28. Real-Time Design and RTOS Basics

A real-time system is correct only if it produces the right result within the required time. “Real-time” does not necessarily mean very fast.

- **Hard deadline:** missing it is unacceptable.
- **Soft deadline:** occasional misses reduce quality but are tolerated.

Analyze worst-case execution time, interrupt latency, scheduling, blocking, and resource contention—not only average speed.

An RTOS commonly provides:

- Tasks/threads
- Priority scheduling
- Queues
- Semaphores
- Mutexes
- Timers
- Event flags

Problems to understand:

- Race condition
- Deadlock
- Starvation
- Priority inversion
- Stack overflow
- Unbounded blocking

A mutex protects shared resources in task context and may support priority inheritance. A semaphore signals availability/events. A queue transfers ownership/data. These are not interchangeable merely because each can block a task.

Keep ISRs short and use RTOS functions explicitly documented as safe “from ISR.”

## 29. Undefined and Implementation-Defined Behavior

Undefined behavior gives the C standard no requirements. Optimization can make its effects surprising.

Common examples:

- Signed integer overflow
- Out-of-bounds array access
- Null or invalid pointer dereference
- Using an uninitialized automatic value
- Modifying a scalar more than allowed between sequence points/evaluations
- Shifting by the width or more
- Violating aliasing rules
- Data races under the C memory model

Implementation-defined behavior requires the implementation to choose and document behavior, such as some type sizes or signed right shift.

Do not test undefined behavior and assume the observed outcome is guaranteed. Prevent it by design, warnings, static analysis, sanitizers on host tests, and careful review.

## 30. Error Handling and Defensive Design

Embedded APIs often return explicit status codes:

```c
typedef enum {
    DRIVER_OK = 0,
    DRIVER_BUSY,
    DRIVER_TIMEOUT,
    DRIVER_INVALID_ARGUMENT,
    DRIVER_HARDWARE_ERROR
} driver_status_t;
```

Validate at trust boundaries:

- Pointers are non-null.
- Lengths fit buffers.
- Enum values and commands are recognized.
- Values are within electrical/physical ranges.
- Arithmetic cannot overflow.
- Timeouts exist for hardware waits.
- External packet length and checksum are valid.

Design safe failure behavior. If a motor controller loses communication, continuing the last command forever may be worse than stopping.

## 31. Fixed-Point Arithmetic

Microcontrollers without suitable floating-point hardware may use fixed-point values.

For Q-format with `F` fractional bits:

```text
stored integer = real value * 2^F
real value = stored integer / 2^F
```

Example Q8.8:

```c
typedef int16_t q8_8_t;

q8_8_t q_from_int(int16_t value)
{
    return (q8_8_t)(value << 8U);
}

q8_8_t q_multiply(q8_8_t a, q8_8_t b)
{
    int32_t product = (int32_t)a * (int32_t)b;
    return (q8_8_t)(product >> 8U);
}
```

Production fixed-point code must define rounding, saturation, negative shifts, overflow bounds, and valid inputs carefully.

## 32. Checksums and CRCs

Checksums detect some accidental corruption. CRCs provide stronger burst-error detection when the same exact parameters are used:

- Polynomial
- Initial value
- Input/output reflection
- Final XOR
- Byte order

A CRC detects errors; it does not provide authenticity or protect against deliberate modification. Security requires an appropriate message authentication code or digital signature plus key management.

## 33. Build Process and Toolchain Outputs

Stages:

1. **Preprocess:** includes headers and expands macros.
2. **Compile:** converts C into assembly/intermediate object code.
3. **Assemble:** creates object files.
4. **Link:** resolves symbols and places sections in memory.
5. **Convert:** optionally creates `.bin` or `.hex` for programming.
6. **Flash:** transfers firmware to the target.
7. **Debug:** controls execution and inspects state.

Useful outputs:

- `.o`/`.obj`: object file
- `.elf`/`.axf`: linked executable with symbols/debug information
- `.map`: symbol and memory-placement map
- `.bin`: raw binary image
- `.hex`: address-aware textual firmware image
- assembly listing/disassembly: generated instructions

Always inspect flash/RAM use and linker-map changes in constrained systems.

Useful compiler options vary, but commonly include:

```text
-Wall -Wextra -Wpedantic    warnings
-Wconversion -Wshadow      additional warning families, introduced carefully
-g                         debug information
-O0                        debug optimization level
-O2 or -Os                 performance or size optimization
-ffunction-sections
-fdata-sections            place functions/data separately
-Wl,--gc-sections          remove unreachable sections at link
```

Test the optimized production configuration; timing and undefined-behavior bugs may differ from a debug build.

## 34. Startup, Vector Table, and Linker Script

The vector table contains the initial stack pointer and exception/interrupt handler addresses on many microcontrollers. Reset selects the reset handler, which performs runtime initialization before `main`.

A linker script describes:

- Flash and RAM origins and sizes
- Section placement
- Stack/heap regions
- Bootloader/application boundaries
- Special retained/no-initialize data
- Symbols used by startup code

These files are hardware-critical. Begin with vendor or SDK versions for the exact device, review them, and version them with the project.

A bootloader may verify and launch an application. Production update systems should consider integrity, authenticity, rollback, interruption during update, compatibility, and recovery.

## 35. Debugging Embedded Systems

### Tools

- Compiler warnings
- Debugger with breakpoints and watchpoints
- SWD/JTAG debug probe
- UART logging
- GPIO timing markers plus oscilloscope/logic analyzer
- Multimeter
- Protocol analyzer
- Map file and disassembly
- Fault/status registers
- Static analysis
- Host sanitizers for portable modules

### A disciplined debugging method

1. State the expected and observed behavior precisely.
2. Make the failure repeatable.
3. Check power, reset, clock, wiring, and pin mapping.
4. Reduce to the smallest failing path.
5. Inspect compiler warnings and return codes.
6. Observe boundary signals and register states.
7. Form one hypothesis and design a test that could disprove it.
8. Fix the root cause.
9. Add a regression test or diagnostic.

Avoid relying on `printf` timing in real-time bugs; logging can change the timing and hide the failure.

### Breakpoint warning

Peripherals, watchdogs, DMA, and other cores may continue running while the CPU is stopped. A breakpoint can therefore change or damage system state. Use peripheral freeze support or safer diagnostics when appropriate.

## 36. Testing Without and With Hardware

### Host unit testing

Separate pure logic from direct register access:

```c
uint16_t temperature_alarm_threshold(uint16_t base, uint16_t margin)
{
    uint32_t result = (uint32_t)base + (uint32_t)margin;
    return (result > UINT16_MAX) ? UINT16_MAX : (uint16_t)result;
}
```

This can run on the desktop with boundary tests.

### Hardware abstraction

Application code should call interfaces such as:

```c
bool button_is_pressed(void);
void motor_set_percent(uint8_t percent);
```

Tests can substitute fake implementations. Hardware-specific source files perform real register access.

### Testing levels

- Unit: one function/module
- Integration: interacting modules or driver plus peripheral
- Hardware-in-the-loop: real target controlled by automated equipment
- System: full product behavior
- Fault injection: timeouts, corrupt packets, missing sensors, low voltage
- Regression: protect previously fixed behavior

Test boundaries: zero, maximum, one beyond maximum, wraparound, empty/full buffer, repeated interrupt, timeout, corrupted input, and reset during operation.

## 37. Coding Style and Safety Standards

Good embedded style:

- Use fixed-width integers where width matters.
- Include units in names: `timeout_ms`, `voltage_mv`.
- Use braces consistently.
- Keep functions small and single-purpose.
- Keep global state private with file-scope `static`.
- Check every meaningful error return.
- Put timeouts on external/hardware waits.
- Avoid magic numbers; name constants from documented requirements.
- Document concurrency, ownership, ranges, and side effects.
- Build warning-free under strict flags.
- Review generated size and critical assembly when necessary.

Safety/security-focused projects may use rules such as MISRA C or CERT C. A rule set is not a substitute for architecture, tests, hazard analysis, or review. Document justified deviations and use tools plus human judgment.

## 38. Suggested Project Structure

```text
firmware/
├── CMakeLists.txt or Makefile
├── linker/
│   └── device.ld
├── startup/
│   └── startup_device.c
├── include/
│   ├── app.h
│   └── board.h
├── src/
│   ├── main.c
│   ├── app.c
│   └── board.c
├── drivers/
│   ├── gpio.c
│   └── uart.c
├── tests/
├── third_party/
└── README.md
```

Keep generated build output in a separate `build/` directory and out of source control unless there is a deliberate release-artifact policy.

## 39. Complete Learning Sequence

### Stage 1: Desktop C foundations

1. Compile and run small programs.
2. Types, operators, conditions, and loops.
3. Functions and scope.
4. Arrays, strings, structs, and enums.
5. Pointers and `const`.
6. Headers and multiple source files.
7. Warnings, debugger, and unit tests.

### Stage 2: Embedded foundations

1. Binary, hex, masks, and shifts.
2. Fixed-width integers and overflow.
3. `volatile`, registers, and memory-mapped I/O.
4. Memory layout, stack, and linker output.
5. GPIO and non-blocking time.
6. State machines and interrupts.
7. Timers, UART, SPI, I2C, and ADC.

### Stage 3: Reliable firmware

1. Ring buffers and interrupt/main concurrency.
2. Watchdogs, reset reasons, and fault handling.
3. Hardware abstraction and host unit tests.
4. DMA, power management, and real-time constraints.
5. Static analysis and safe coding rules.
6. Boot/update design and production diagnostics.

### Stage 4: Board-specific mastery

1. Read the board schematic.
2. Read the exact MCU datasheet and reference manual.
3. Learn the vendor SDK and startup/linker files.
4. Configure and verify clocks.
5. Bring up one peripheral at a time.
6. Use SWD/JTAG and electrical test instruments.
7. Measure timing, memory, power, and fault recovery.

## 40. Practice Projects

Do these in order:

1. Desktop calculator with separate `.c` and `.h` files.
2. Bit-mask program that sets, clears, toggles, and tests flags.
3. GPIO LED blink using a hardware timer rather than a long delay.
4. Debounced button controlling an LED state machine.
5. UART echo with a ring buffer and overflow handling.
6. Periodic ADC sampling with min/mean/max calculations.
7. PWM brightness or motor-speed control with safe limits.
8. I2C or SPI sensor driver with timeout and error codes.
9. Packet protocol with length, sequence number, and CRC.
10. Data logger using double buffering/DMA where supported.
11. Watchdog-supervised system with stored reset cause.
12. Boot-safe firmware update design for your chosen board.

For every project, write:

- Requirements and timing constraints
- Pin/peripheral assignments
- State machine or architecture
- Error and safe-state behavior
- Test cases
- Flash/RAM usage
- Known limitations

## 41. Common Interview and Exam Questions

### Why is `volatile` used?

It forces observable accesses to an object that may change outside ordinary code flow, such as a hardware register or ISR-shared flag. It does not make compound access atomic or thread-safe.

### What is the difference between `const` and `volatile`?

`const` prevents modification through a particular access path. `volatile` says accesses cannot be optimized away or freely combined because the value may change externally. A register can be both, such as a read-only status register.

### What does file-scope `static` do?

It gives a name internal linkage, making it private to that source file. A static local instead preserves its value across calls.

### Macro versus inline function?

A macro is token substitution without normal type checking and can evaluate arguments more than once. A `static inline` function has function semantics, types, and single evaluation while still allowing inlining.

### Why avoid dynamic allocation?

It may cause fragmentation, nondeterministic timing, failure, and ownership bugs. Fixed pools/static buffers often give predictable embedded behavior.

### Polling versus interrupts?

Polling repeatedly checks an event and is simple but can waste CPU or add latency. Interrupts react asynchronously and improve responsiveness but add concurrency and timing complexity.

### What is a race condition?

The result depends on the timing/order of unsynchronized accesses to shared state. `volatile` alone does not fix it.

### What is interrupt latency?

Time from the interrupt event to execution of its handler. It is affected by masking, current instructions, higher-priority interrupts, entry overhead, and critical sections.

### What is a watchdog?

A hardware timer that resets or faults the system when software does not prove continued health within the required interval.

### What is memory-mapped I/O?

Hardware registers occupy addresses in the processor's memory space and are accessed through appropriately qualified register definitions.

### What happens before `main`?

After reset, startup code establishes the stack/runtime, copies initialized data to RAM, clears zero-initialized data, may initialize clocks/runtime features, and then calls `main`.

### Why is unsigned subtraction useful for timers?

Modulo unsigned arithmetic allows `(now - then) >= interval` to keep working across counter wraparound when the design respects the valid interval range.

### What is endianness?

The byte order used to store a multi-byte value. Protocols should encode byte order explicitly instead of copying native structs.

### What is undefined behavior?

Behavior for which the C standard gives no requirements, such as signed overflow or out-of-bounds access. The compiler may optimize assuming it never occurs.

### Why use a cross-compiler?

The host computer and target microcontroller have different instruction sets, ABI, memory layout, and runtime. A cross-compiler produces code for the target.

## 42. Quick Reference

| Task | Pattern |
|---|---|
| Set bit `n` | `reg |= (UINT32_C(1) << n);` |
| Clear bit `n` | `reg &= ~(UINT32_C(1) << n);` |
| Toggle bit `n` | `reg ^= (UINT32_C(1) << n);` |
| Test bit `n` | `(reg & (UINT32_C(1) << n)) != 0U` |
| Array element count | `sizeof a / sizeof a[0]` (only where `a` is an array) |
| Zero initialize | `type object = {0};` |
| Width-specific type | `uint8_t`, `int16_t`, `uint32_t` |
| Read-only input buffer | `const uint8_t *data` |
| File-private function | `static void helper(void)` |
| Externally changing object | `volatile` plus proper synchronization |
| Wrap-safe elapsed time | `(uint32_t)(now - then) >= interval` |
| Widen multiply | `(uint32_t)a * (uint32_t)b` |
| Compile desktop C | `clang -std=c17 -Wall -Wextra file.c -o app.exe` |
| Syntax check | `clang -std=c17 -Wall -Wextra -fsyntax-only file.c` |

## 43. Test-Day Checklist

Be ready to explain:

- Desktop compiler versus embedded cross-compiler
- Compile, assemble, link, flash, and debug stages
- Fixed-width integer types and integer promotion
- Scope, storage duration, linkage, `static`, and `extern`
- Arrays versus pointers and why lengths must be passed
- `const`, `volatile`, and why volatile is not synchronization
- Bit masks, shifts, set/clear/toggle/test operations
- Stack, heap, `.text`, `.rodata`, `.data`, and `.bss`
- Memory-mapped registers and read-modify-write hazards
- Endianness, alignment, padding, and serialization
- Super loops, non-blocking timing, and state machines
- Interrupt design, atomicity, critical sections, and ring buffers
- GPIO, timers/PWM, ADC, UART, SPI, I2C, and DMA
- Watchdogs, reset causes, fault handling, and safe states
- Real-time deadlines and RTOS concurrency hazards
- Undefined behavior and defensive C
- Host tests, hardware tests, debugging tools, and static analysis

## 44. Golden Rules

1. Read the exact datasheet, reference manual, schematic, and errata for the target.
2. Compile with strong warnings and fix them deliberately.
3. Use unsigned fixed-width types for register work.
4. Keep ISRs short and move substantial work to normal context.
5. Put a timeout on every hardware or communication wait.
6. Never assume `volatile` makes shared data safe.
7. Avoid hidden allocation and unbounded execution in real-time paths.
8. Validate external lengths, commands, and values before use.
9. Encode protocols explicitly; never transmit raw structs blindly.
10. Design the safe state and failure behavior before the happy path.
11. Test boundary cases, optimized builds, actual hardware, and recovery paths.
12. Measure timing, stack, memory, power, and electrical signals instead of guessing.

Master ordinary C first, then learn how the compiler, memory map, peripherals, interrupts, electrical hardware, and timing interact. That combination—not just C syntax—is embedded programming.
