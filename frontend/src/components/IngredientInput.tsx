import { useState, type FormEvent } from 'react';
import { Button } from '@/components/ui/Button';
import { Card, StepHeading } from '@/components/ui/Card';
import { RemovableChip } from '@/components/ui/Chip';
import { fieldClass } from '@/components/ui/field';

const QUICK_ADD = ['onion', 'garlic', 'tomato', 'chicken', 'rice', 'pasta', 'egg', 'cheese'];

interface IngredientInputProps {
  ingredients: string[];
  onIngredientsChange: (ingredients: string[]) => void;
}

export default function IngredientInput({ ingredients, onIngredientsChange }: IngredientInputProps) {
  const [inputValue, setInputValue] = useState('');

  const add = (name: string) => {
    const ingredient = name.trim().toLowerCase();
    if (ingredient && !ingredients.includes(ingredient)) {
      onIngredientsChange([...ingredients, ingredient]);
    }
  };

  const remove = (ingredient: string) => {
    onIngredientsChange(ingredients.filter((i) => i !== ingredient));
  };

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    add(inputValue);
    setInputValue('');
  };

  return (
    <Card>
      <StepHeading step={1} title="Your ingredients" />

      <form onSubmit={handleSubmit} className="flex gap-2">
        <label htmlFor="ingredient" className="sr-only">Ingredient</label>
        <input
          id="ingredient"
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          placeholder="Add an ingredient, e.g. chickpeas"
          className={`h-13 min-w-0 flex-1 px-4.5 text-base ${fieldClass}`}
        />
        <Button type="submit" disabled={!inputValue.trim()} className="h-13 px-6">
          Add
        </Button>
      </form>

      {ingredients.length > 0 && (
        <div className="flex flex-wrap gap-2">
          {ingredients.map((ingredient) => (
            <RemovableChip key={ingredient} label={ingredient} onRemove={() => remove(ingredient)} />
          ))}
        </div>
      )}

      <div className="flex flex-col gap-2.5">
        <span className="text-sm text-muted">Quick add</span>
        <div className="flex flex-wrap gap-2">
          {QUICK_ADD.map((name) => (
            <button
              type="button"
              key={name}
              onClick={() => add(name)}
              disabled={ingredients.includes(name)}
              className="h-9 rounded-[10px] border border-field-line bg-field px-3.5 text-sm transition-opacity disabled:opacity-40"
            >
              + {name}
            </button>
          ))}
        </div>
      </div>
    </Card>
  );
}
