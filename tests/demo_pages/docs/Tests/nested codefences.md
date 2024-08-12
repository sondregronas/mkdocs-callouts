# Nested codefences

Codefences get treated like normal text when they are inside a callout. This means you can display the callout syntax inside a codefence without it being rendered as a callout.

(This is here because they used to be rendered as callouts in the past)

> [!NOTE] Callout syntax with a nested codefence
> ```md
> > [!WARNING]
> > This is a warning inside a codefence
> ```

> [!NOTE] Callout syntax
> > [!WARNING]
> > This is a warning inside a codefence

> [!NOTE] Callout syntax with a nested codefence
> ```md
> > [!WARNING]
> > This is a warning inside a codefence
> ```

```md
> [!NOTE] Callout syntax with a nested codefence
> ```md
> > [!WARNING]
> > This is a warning inside a codefence
> ```

> [!NOTE] Callout syntax
> > [!WARNING]
> > This is a warning inside a codefence

> [!NOTE] Callout syntax with a nested codefence
> ```md
> > [!WARNING]
> > This is a warning inside a codefence
> ```
```