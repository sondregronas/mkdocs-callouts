# More blockquotes

Nesting blockquotes and callouts can be very tricky and messy, so you probably shouldn't do stuff like this, but here's just an extreme example.

> > > > This is a blockquote.
> > > > [!NOTE]
> > > > This is a nested note inside 3 blockquotes.
> > > > > It also has a blockquote
> 
> > > > > > [!TIP]
> > > > > > The tip is nested inside the note, which is nested inside the blockquote.
> 
> First level blockquote
> 
> > [!TIP]
> > > This is a blockquote inside a tip inside a blockquote.
> [!WARNING]
> This is a warning outside a blockquote.

> > [!TIP]
> > ```md
> > > [!WARNING]
> > > This is a codeblock inside a blockquote inside a tip, note how the callout syntax is not converted.
> > ```
> 
> > > [!WARNING]
> > > This does get converted, since its not inside a codeblock.


## Source

```md
> > > > This is a blockquote.
> > > > [!NOTE]
> > > > This is a nested note inside 3 blockquotes.
> > > > > It also has a blockquote
> 
> > > > > > [!TIP]
> > > > > > The tip is nested inside the note, which is nested inside the blockquote.
> 
> First level blockquote
> 
> > [!TIP]
> > > This is a blockquote inside a tip inside a blockquote.
> [!WARNING]
> This is a warning outside a blockquote.

> > [!TIP]
> > ```md
> > > [!WARNING]
> > > This is a codeblock inside a blockquote inside a tip, note how the callout syntax is not converted.
> > ```
> 
> > > [!WARNING]
> > > This does get converted, since its not inside a codeblock.
```

> [!NOTE] Sidenote: codefences inside codefences messes with the logic
> The syntax inside codefences (inside codefences) get converted, even though they shouldn't.