# Edgecases

Things that might break

### `>` symbol in callout

> [!INFO] > in title
> This is a callout with a `>` symbol in the title

### Callout syntax as title

> [!NOTE] > [!WARNING]
> This is a callout with a callout syntax as title


### No whitespace
>[!NOTE]No whitespace
>This is a callout without whitespace

### Excess whitespace
  >    [!NOTE] Excess whitespace
 >  This is a callout with excess whitespace


## Source

```md
### `>` symbol in callout

> [!INFO] > in title
> This is a callout with a `>` symbol in the title

### Callout syntax as title

> [!NOTE] > [!WARNING]
> This is a callout with a callout syntax as title


### No whitespace
>[!NOTE]No whitespace
>This is a callout without whitespace

### Excess whitespace
  >    [!NOTE] Excess whitespace
 >  This is a callout with excess whitespace
```